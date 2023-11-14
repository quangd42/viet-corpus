import sys
import datetime
import json


# Maximum number of output file
OUTPUT_COUNT_LIMIT = 1
OUTPUT_PATH = "data/output/"


def main():

    input_file, number_of_lines = validate_usage()

    telex_mapping = load_telex_mapping("/Users/quang-dang/Documents/viet-corpus-converter/telex-converter/new_telex_mapping.json")
    if not validate_telex_mapping(telex_mapping):
        sys.exit('telex_mapping contains invalid info')
    
    output_filenames = convert_multiple_lines_to_telex(input_file, telex_mapping, number_of_lines)
    print(f"{len(output_filenames) - 1} files created successfully. Output written to {OUTPUT_PATH}.")


def validate_usage() -> tuple:
    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py <input_file> <number_of_lines>")
    else:
        input_file = sys.argv[1]
        number_of_lines = int(sys.argv[2])
        return input_file, number_of_lines


def load_telex_mapping(input_file: str) -> dict:
    try:
        with open(input_file) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit("Mapping file not found, loading failed.")



def validate_telex_mapping(mapping: dict) -> bool:
    mapping = mapping['mapping']
    for item in mapping:
        if item['mod'] not in ['a', 'e', 'o', 'w', 'd', '']:
            print(f"Error with {item['name']}")
            return False
        if item['diacritics'] not in ['s', 'f', 'r', 'x', 'j', '']:
            print(f"Error with {item['name']}")
            return False
        if len(item['name']) == 2 and item['name'][-1] != item['main'][-1]:
            if item['main'] == 'uo':
                pass
            else:
                print(f"Error with {item['name']}")
                return False
            
    return True
        

def convert_word_to_telex(word: str, telex_mapping_json: dict) -> str:
    telex_word = ''
    i = 0
    word_len = len(word)
    try:
        telex_mapping = telex_mapping_json['mapping']
    except IndexError:
        sys.exit('Mapping does not exist.')

    while i < word_len:
        found = False
        for j in range(min(5, word_len - i), 0, -1):
            subword = word[i:i+j]
            for vowel in telex_mapping:
                if subword == vowel['name']:
                    
                    telex_word += vowel['main'] + vowel['mod'] + vowel['diacritics']
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


def convert_multiple_lines_to_telex(input_file: str, telex_mapping: dict, number_of_lines: int) -> int:
    try:
        with open(input_file, encoding="utf-8") as f:
            output_filenames = []
            telex_lines = []
            
            for line in f:
                telex_line = convert_line_to_telex(line, telex_mapping)
                telex_lines.append(telex_line)

                if len(telex_lines) == number_of_lines:
                    output_filenames = save_telex_output(telex_lines, output_filenames)
                    telex_lines = []

                if len(output_filenames) == OUTPUT_COUNT_LIMIT:
                    break
        
        return output_filenames

    except FileNotFoundError:
        sys.exit("Input file not found.")
    except Exception as e:
        sys.exit("An error occurred:", str(e))


def save_telex_output(telex_lines: list, output_filenames: list) -> list:
    today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_count = len(output_filenames) + 1
    output_file = OUTPUT_PATH + "telex_output" + "_" + today + "_" + str(output_count) + "." + "txt"
    with open(output_file, 'w', encoding="utf-8") as f_out:
        f_out.write("\n".join(telex_lines))
    print(f"Created {output_file}.")
    output_filenames.append(output_file)
    return output_filenames


if __name__ == "__main__":
    main()
