"""Convert Vietnamese text to the telex input"""

import sys
import datetime
import json
from pathlib import Path


LINE_COUNT_PER_FILE = 3000
OUTPUT_PATH = Path("./data/output/batch2").resolve()
MAPPING_PATH = Path("./new_telex_mapping-w.json").resolve()


def main():
    input_file, line_count_limit = validate_usage()

    telex_mapping = load_telex_mapping(MAPPING_PATH)
    if not validate_telex_mapping(telex_mapping):
        sys.exit("telex_mapping contains invalid info")

    output_path = OUTPUT_PATH
    Path.mkdir(output_path, parents=True, exist_ok=True)

    output_count = convert_and_save(
        input_file, telex_mapping, line_count_limit, output_path
    )

    print(f"{'-' * 5}")
    if output_count == 0:
        print("No file created. Something went wrong.")
    else:
        print(
            f"{output_count} files created successfully. Output written to {output_path}"
        )


def validate_usage() -> tuple:
    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py <input_file> <line_count_limit>")
    else:
        input_file = sys.argv[1]
        line_count_limit = int(sys.argv[2])
        return input_file, line_count_limit


def load_telex_mapping(input_file: Path) -> dict:
    try:
        with open(input_file) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit("Mapping file not found, loading failed.")


def validate_telex_mapping(mapping: dict) -> bool:
    mapping = mapping["mapping"]
    for item in mapping:
        if item["mod"] not in ["a", "e", "o", "w", "d", ""]:
            print(f"Error with {item['name']}")
            return False
        if item["diacritics"] not in ["s", "f", "r", "x", "j", ""]:
            print(f"Error with {item['name']}")
            return False
        if len(item["name"]) == 2 and item["name"][-1] != item["main"][-1]:
            if item["main"] == "uo" or item["main"] == "wo":
                pass
            else:
                print(f"Error with {item['name']}")
                return False

    return True


def convert_word_to_telex(word: str, telex_mapping_json: dict) -> str:
    telex_word = ""
    i = 0
    word_len = len(word)
    try:
        telex_mapping = telex_mapping_json["mapping"]
    except IndexError:
        sys.exit("Mapping does not exist.")

    while i < word_len:
        found = False
        for j in range(min(5, word_len - i), 0, -1):
            subword = word[i : i + j]
            for vowel in telex_mapping:
                if subword == vowel["name"]:
                    telex_word += vowel["main"] + vowel["mod"] + vowel["diacritics"]
                    i += j
                    found = True
                    break

        if not found:
            telex_word += word[i]
            i += 1

    return telex_word


def convert_line_to_telex(line: str, telex_mapping: dict) -> str:
    words = line.split()
    telex_line = [convert_word_to_telex(word.lower(), telex_mapping) for word in words]
    return " ".join(telex_line)


def save_telex_file(telex_text: str, output_file: Path) -> bool:
    try:
        with open(output_file, "w", encoding="utf-8") as f_out:
            # print("File opened.")
            f_out.write(telex_text)
            print(f"Created {output_file}.")
    except BaseException as err:
        print(f"Failed to save file. {err}")
        return False
    return True


def convert_and_save(
    input_file: str, telex_mapping: dict, line_count_limit: int, output_path: Path
) -> int:
    try:

        output_count = 0
        today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(input_file, encoding="utf-8") as f:
            telex_lines = []
            line_count = 0

            for line in f:
                line_count += 1
                if line_count > line_count_limit:
                    break

                telex_lines.append(convert_line_to_telex(line, telex_mapping))

                if len(telex_lines) == LINE_COUNT_PER_FILE:
                    output_name = f"telex_output_{today}_{output_count}.txt"
                    output_file = output_path / output_name
                    if save_telex_file("\n".join(telex_lines), output_file):
                        output_count += 1
                    telex_lines.clear()

            if len(telex_lines) > 0:
                output_name = f"telex_output_{today}_{output_count}.txt"
                output_file = output_path / output_name
                if save_telex_file("\n".join(telex_lines), output_file):
                    output_count += 1

        return output_count

    except FileNotFoundError:
        sys.exit("Input file not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
