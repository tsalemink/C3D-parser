import os
import platform
import argparse

import PySide6 as RefMod

import PyInstaller.__main__

from c3d_parser.settings.general import APPLICATION_NAME


# Set Python optimisations on.
os.environ['PYTHONOPTIMIZE'] = '1'

here = os.path.dirname(__file__)


def main():
    run_command = [
        '../../src/c3d_parser/application.py',
        '-n', f'{APPLICATION_NAME}',
        '--windowed',
        '--noconfirm',
    ]

    pyside_dir = os.path.dirname(RefMod.__file__)

    if platform.system() == 'Darwin':
        rcc_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "rcc")
        uic_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "uic")

    elif platform.system() == "Windows":
        rcc_exe = os.path.join(pyside_dir, "rcc.exe")
        uic_exe = os.path.join(pyside_dir, "uic.exe")

    else:
        raise NotImplementedError("Platform is not supported for creating this application.")

    run_command.append(os.pathsep.join([f'--add-binary={rcc_exe}', 'PySide6/']))
    run_command.append(os.pathsep.join([f'--add-binary={uic_exe}', 'PySide6/']))

    json_files = os.path.join('../../src/c3d_parser/core/marker_maps', '*.json')
    run_command.append(os.pathsep.join([f'--add-data={json_files}', 'c3d_parser/core/marker_maps/']))

    print('Running command: ', run_command)
    PyInstaller.__main__.run(run_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="create_application")
    args = parser.parse_args()

    main()