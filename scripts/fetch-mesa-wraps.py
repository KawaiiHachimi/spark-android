#!/usr/bin/env python3
"""Populate the captured Mesa offline packagefiles directory with SHA256 checks."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

PACKAGE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Android source root')
    parser.add_argument('--check', action='store_true', help='only validate existing archives')
    args = parser.parse_args()
    destination = args.source.resolve() / 'external/mesa/subprojects/packagefiles'
    if not (destination.parent.parent / 'meson.build').is_file():
        parser.error('external/mesa is missing')
    destination.mkdir(parents=True, exist_ok=True)
    failures = []
    for item in json.loads((PACKAGE / 'support/mesa-wraps.json').read_text()):
        if not item['captured']:
            continue
        target = destination / item['filename']
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256']:
            print('OK', target.name)
            continue
        if args.check:
            failures.append(target.name)
            continue
        errors = []
        for url in item['urls']:
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    data = response.read()
                if hashlib.sha256(data).hexdigest() != item['sha256']:
                    raise ValueError('SHA256 mismatch')
                temporary = target.with_suffix(target.suffix + '.part')
                temporary.write_bytes(data)
                temporary.replace(target)
                print('FETCHED', target.name)
                break
            except Exception as error:
                errors.append(f'{url}: {error}')
        else:
            failures.append(target.name + ': ' + '; '.join(errors))
    if failures:
        raise SystemExit('Missing or invalid archives:\n' + '\n'.join(failures))


if __name__ == '__main__':
    main()
