#!/usr/bin/env python3
"""Check or apply the pinned per-repository Spark patch series."""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]


def git(repo, *args, env=None, data=None):
    result = subprocess.run(['git', '-C', str(repo), *args], env=env,
                            input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"{repo}: git {' '.join(args)}\n{result.stderr.decode()}")
    return result.stdout.decode().strip()


def patch_bytes(item):
    path = PACKAGE / item['file']
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != item['sha256']:
        raise RuntimeError(f'Patch checksum mismatch: {path}')
    return lzma.decompress(raw) if path.suffix == '.xz' else raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Android source root')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='validate clean bases and replay in temporary indexes')
    mode.add_argument('--apply', action='store_true', help='preflight every repository, then apply using git am')
    mode.add_argument('--verify-package', action='store_true', help='replay base objects without requiring checkout at base')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    lock = json.loads((PACKAGE / 'sources.lock.json').read_text())
    report = []
    # Finish preflight for every repository before any checkout is modified.
    for item in lock['projects']:
        repo = source / item['path']
        if git(repo, 'rev-parse', '--show-toplevel') != str(repo):
            raise RuntimeError(f'Not a standalone repository: {repo}')
        if not args.verify_package:
            if git(repo, 'rev-parse', 'HEAD') != item['base']:
                raise RuntimeError(f"{repo}: expected clean base {item['base']}")
            if git(repo, 'status', '--porcelain', '--untracked-files=no'):
                raise RuntimeError(f'{repo}: tracked changes exist')
            for marker in ('rebase-apply', 'rebase-merge', 'MERGE_HEAD', 'CHERRY_PICK_HEAD'):
                marker_path = git(repo, 'rev-parse', '--path-format=absolute', '--git-path', marker)
                if Path(marker_path).exists():
                    raise RuntimeError(f'{repo}: operation already in progress ({marker})')
        with tempfile.TemporaryDirectory(prefix='spark-patch-check-') as directory:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(directory) / 'index'))
            git(repo, 'read-tree', item['base'], env=env)
            for patch in item['patches']:
                git(repo, 'apply', '--cached', '--whitespace=nowarn', '-', env=env, data=patch_bytes(patch))
            tree = git(repo, 'write-tree', env=env)
            if tree != item['tree']:
                raise RuntimeError(f"{repo}: replayed tree {tree} != captured tree {item['tree']}")
        report.append(dict(path=item['path'], patches=len(item['patches']), tree=tree, result='PASS'))
        print(f"PASS {item['path']}: {len(item['patches'])} patches, tree {tree}", flush=True)
    if args.apply:
        for item in lock['projects']:
            repo = source / item['path']
            for patch in item['patches']:
                git(repo, 'am', '--whitespace=nowarn', data=patch_bytes(patch))
            if git(repo, 'rev-parse', 'HEAD^{tree}') != item['tree']:
                raise RuntimeError(f'{repo}: unexpected result after git am')
            print(f"APPLIED {item['path']}", flush=True)
    if args.report:
        args.report.write_text(json.dumps(dict(mode='apply' if args.apply else 'verify-package' if args.verify_package else 'check',
                                               repositories=report), indent=2) + '\n')


if __name__ == '__main__':
    main()
