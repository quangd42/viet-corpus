import subprocess
import shutil
from pathlib import Path

# Genkey main.go path
genkey_folder_path = "/Users/quang-dang/Documents/genkey/"
genkey_executable = genkey_folder_path + "genkey"
genkey_data_json = genkey_folder_path + "data.json"

combiner_input_path = "/Users/quang-dang/Documents/viet-corpus-converter/corpus-json-combiner/data/input/batch1/"

input_path = Path("/Users/quang-dang/Documents/viet-corpus-converter/telex-converter/data/output/batch1/")
file_list = list(input_path.glob("*.txt"))

for input_file in file_list:
    # Arguments to pass
    # input_file = file_list[0]
    args = ["load", input_file]

    # Run genkey
    # print([genkey_executable] + args)
    subprocess.run([genkey_executable] + args)

    # Copy data.json file to this directory
    index = file_list.index(input_file)
    # print(index)
    shutil.copyfile(genkey_data_json, combiner_input_path + "data_" + str(index) + ".json")

