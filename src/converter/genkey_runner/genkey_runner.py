"""Run genkey to analyze all txt files in a dir"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Genkey path
# This needs to be hard coded to reuse genkey load function
GENKEY_FOLDER_PATH = Path('./genkey').resolve()


def main():
    input_path = validate_usage()
    if not check_genkey_exist(GENKEY_FOLDER_PATH):
        sys.exit('Cannot find genkey executable.')
    file_list = get_input_file_list(input_path)
    output_path = create_output_dir(input_path)
    output_files = run_genkey(file_list, output_path, GENKEY_FOLDER_PATH)

    print(output_files)


def validate_usage() -> Path:
    if len(sys.argv) != 2:
        sys.exit('Usage: python main.py <input_dir_path>')
    else:
        input_dir_path = sys.argv[1]
        return Path(input_dir_path)


def get_input_file_list(input_dir_path: Path) -> list[Path]:
    return list(input_dir_path.glob('*.txt'))


def create_output_dir(input_path: Path) -> Path:
    output_path = input_path / 'genkey'
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def check_genkey_exist(genkey_folder_path: Path):
    genkey_executable = genkey_folder_path / 'genkey'
    return genkey_executable.exists()


def run_genkey(
    file_list: list[Path], output_path: Path, genkey_folder_path: Path
) -> list[Path]:
    output_files: list[Path] = []
    genkey_executable = genkey_folder_path / 'genkey'

    for input_file in file_list:
        filename, _ = input_file.name.split('.')

        # Arguments to pass
        args: list[str | Path] = ['load', input_file.resolve()]

        # Run genkey
        subprocess.run([genkey_executable] + args, cwd=genkey_folder_path)

        # Copy json output file to this directory
        filename = f'{filename}.json'
        source_file = genkey_folder_path / 'corpora' / filename
        output_file = output_path / filename
        shutil.copyfile(source_file, output_file)
        os.remove(source_file)

        output_files.append(output_file)

    return output_files


if __name__ == '__main__':
    main()
