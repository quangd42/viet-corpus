import subprocess
import shutil
from pathlib import Path

# Genkey main.go path
genkey_folder_path = "/Users/quang-dang/Documents/genkey/"
genkey_executable = genkey_folder_path + "genkey"
genkey_data_json = genkey_folder_path + "data.json"

output_path = "/Users/quang-dang/Documents/viet-corpus-converter/corpus-json-combiner/data/input/test_batch1/"

input_path = Path("/Users/quang-dang/Documents/viet-corpus-converter/telex-converter/data/output/batch1/")
file_list = list(input_path.glob("*.txt"))


def main():
    create_output_dir(output_path)
    output_files = run_genkey(file_list, output_path)

    print(output_files)


def create_output_dir(output_path: str) -> None:
    Path(output_path).mkdir(parents=True, exist_ok=True)


def run_genkey(file_list: list, output_path: str) -> list:
    output_files = []
    
    for input_file in file_list:
        

        # Arguments to pass
        args = ["load", input_file]

        # Run genkey
        subprocess.run([genkey_executable] + args)

        # Copy data.json file to this directory
        index = file_list.index(input_file)
        filename = f"data_{str(index)}.json"
        output_file = Path(output_path) / filename
        shutil.copyfile(genkey_data_json, output_file)

        output_files.append(output_file)
    
    return output_files


if __name__ == "__main__":
    main()