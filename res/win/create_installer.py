import argparse
import os
import sys
import subprocess
import tempfile

from c3d_parser.settings.general import APPLICATION_NAME


class ReplaceOnlyDict(dict):

    def __missing__(self, key):
        return '{' + key + '}'


def run_build(pyi_config, spec_file, **kwargs):
    import PyInstaller.building.build_main
    PyInstaller.building.build_main.main(pyi_config, spec_file, **kwargs)


def run_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(p.stdout.readline, ''):
        yield stdout_line

    return_code = p.wait()
    yield 'command returned with value: %s' % return_code


def run_makensis(repo_root_dir, app_version):
    if not os.path.exists(os.path.join(repo_root_dir, 'package')):
        os.mkdir(os.path.join(repo_root_dir, 'package'))

    nsis_exe = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'BIN', 'makensis.exe')
    if os.path.exists(nsis_exe):
        # Create NSIS script from template
        with tempfile.NamedTemporaryFile(delete=False) as outputfile:
            with open(os.path.join(repo_root_dir, 'res', 'win', 'nsis.nsi.template')) as f:
                contents = f.read()

            match_keys = ReplaceOnlyDict(application_version=app_version,
                                         dist_dir=os.path.join(repo_root_dir, 'res', 'pyinstaller', 'dist', APPLICATION_NAME),
                                         win_res_dir=os.path.join(repo_root_dir, 'res', 'win'),
                                         package_dir=os.path.join(repo_root_dir, 'package'))
            formatted_contents = contents.format_map(match_keys)
            outputfile.write(formatted_contents.encode())
            outputfile.flush()
            for line in run_command([nsis_exe, outputfile.name]):
                print(line.strip())

        if os.path.isfile(outputfile.name):
            os.remove(outputfile.name)


if __name__ == '__main__':
    '''
    Create a Windows application installer with NSIS and PyInstaller.
    '''
    parser = argparse.ArgumentParser(prog="create_installer")
    parser.add_argument("version", help="Application version")
    args = parser.parse_args()

    here = os.path.realpath(os.path.dirname(__file__))

    root_dir = os.path.realpath(os.path.join(here, '..', '..'))

    src_dir = os.path.join(root_dir, 'src')
    sys.path.append(src_dir)

    run_makensis(root_dir, args.version)
