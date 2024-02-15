import sys
import datetime
import json
from pathlib import Path


OUTPUT_PATH = Path("./data/output/batch2").resolve()
MAPPING_PATH = Path("./new_telex_mapping-w.json").resolve()


def main():
    input_file, number_of_lines = validate_usage()

    telex_mapping = load_telex_mapping(MAPPING_PATH)
    if not validate_telex_mapping(telex_mapping):
        sys.exit("telex_mapping contains invalid info")

    telex_text_list = convert_multiple_lines_to_telex(
        input_file, telex_mapping, number_of_lines
    )
    output_file_count = save_telex_output(telex_text_list, OUTPUT_PATH)
    print(
        f"{output_file_count} files created successfully. Output written to {OUTPUT_PATH}."
    )


def validate_usage() -> tuple:
    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py <input_file> <number_of_lines>")
    else:
        input_file = sys.argv[1]
        number_of_lines = int(sys.argv[2])
        return input_file, number_of_lines


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


def convert_multiple_lines_to_telex(
    input_file: str, telex_mapping: dict, number_of_lines: int
) -> list:
    try:
        telex_text_list = []
        with open(input_file, encoding="utf-8") as f:
            telex_lines = []

            for line in f:
                # telex_line = convert_line_to_telex(line, telex_mapping)
                telex_lines.append(convert_line_to_telex(line, telex_mapping))

                if len(telex_lines) == number_of_lines:
                    # output_files = save_telex_output(telex_lines, output_files)
                    # Instead of calling save_telex_output here, put it in memory
                    # This way the program may use up a lot of memory
                    # The function will return list of str instead
                    # TODO: see if yield will help with this
                    break

            telex_text_list.append("\n".join(telex_lines))

        return telex_text_list

    except FileNotFoundError:
        sys.exit("Input file not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {str(e)}")


def save_telex_output(telex_text_list: list[str], output_path: Path) -> int:
    output_count = 0

    for telex_text in telex_text_list:
        today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"telex_output_{today}_{str(output_count)}.txt"
        output_file = output_path / output_name

        try:
            with open(output_file, "w", encoding="utf-8") as f_out:
                # print("File opened.")
                f_out.write(telex_text)
                print(f"Created {output_file}.")
        except BaseException as err:
            sys.exit(f"Failed to save file. {err}")
        output_count += 1
    return output_count


if __name__ == "__main__":
    main()
