#!/usr/bin/env python
import argparse
import glob
import os
import os.path
import platform
import subprocess
import sys
import urllib.request


here = os.path.abspath(os.path.dirname(__file__))


def main():
    parser = argparse.ArgumentParser(prog="release_preparation")
    parser.add_argument("c3d_parser_release", help="tag from C3D-Parser codebase")
    parser.add_argument('-l', '--local', help='absolute path to locally available C3D-Parser')
    parser.add_argument("--pre", action='store_true', help="Allow pre-release versions")
    args = parser.parse_args()

    cut_short = False
    local_c3d_parser = args.local

    available_pips = glob.glob(os.path.join(os.path.dirname(sys.executable), 'pip*'))
    if len(available_pips) == 0:
        sys.exit(1)

    pip = available_pips[0]

    result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print(' == result install:', result.returncode, flush=True)

    # Always install numpy and PySide6.
    result = subprocess.run([pip, "install", "numpy", "PySide6"])
    print(' == result install extras:', result.returncode, flush=True)

    opensim_wheel_url = "https://auckland.figshare.com/ndownloader/files/53096879"
    opensim_wheel_file = "opensim-4.5-py3-none-any.whl"
    urllib.request.urlretrieve(opensim_wheel_url, opensim_wheel_file)
    result = subprocess.run([pip, "install", opensim_wheel_file])
    print(' == result install OpenSim API:', result.returncode, flush=True)

    if local_c3d_parser is None:
        c3d_parser_url = "https://github.com/tsalemink/C3D-parser"
        result = subprocess.run(["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", c3d_parser_url, "-b", args.c3d_parser_release])
        print(' == result git:', result.returncode, flush=True)

    result = subprocess.run([pip, "install", "-e", "."])
    print(' == result install:', result.returncode, flush=True)

    working_env = os.environ.copy()

    if cut_short:
        return

    current_directory = os.getcwd()

    os.chdir(f"res/pyinstaller/")

    result = subprocess.run([sys.executable, "create_application.py"], env=working_env)
    print(' == result application creation:', result.returncode, flush=True)
    os.chdir(current_directory)
    if result.returncode:
        sys.exit(result.returncode)

    # Define a release name from the release tag
    tag = args.c3d_parser_release
    tag_parts = tag[1:].split('.')
    release_name = '.'.join(tag_parts[:3])

    if platform.system() == "Windows":
        os.chdir(f"res/win")
        result = subprocess.run([sys.executable, "create_installer.py", release_name], env=working_env)
        print(' == result create installer:', result.returncode, flush=True)
        os.chdir(current_directory)

    if result.returncode:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
