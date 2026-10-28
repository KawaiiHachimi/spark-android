#!/usr/bin/env python3
"""Extract GB20B auxiliaries using NVIDIA's matching 610.43.03 script.

Arguments: NVIDIA extraction script, OpenRM source directory, output directory.
The source directory must contain the GB20B GspRmBoot and production FMC
generated C files from the NVIDIA 610.43.03 tag. Copy gsp_ga10x.bin and
ucodes_ga10x.bin from the matching .run firmware directory separately.
"""
import importlib.util
import os
import pathlib
import sys

script, source, output = (pathlib.Path(p).resolve() for p in sys.argv[1:])
spec = importlib.util.spec_from_file_location("nvidia_extract", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
os.chdir(source)
module.outputpath = str(output)
module.version = "610.43.03"
module.gsp_bootloader("gb20b", "prod")
module.fmc("gb20b", "Prod")
