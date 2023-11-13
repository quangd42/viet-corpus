import matplotlib.pyplot as plt

import json, sys, os


EXPORT_KEY_LIST = ['letters', 'bigrams', 'trigrams', 'skipgrams']
# EXPORT_KEY_LIST = ['letters']


def main():
    # Load json file to dict
    validate_input()
    input_file = str(sys.argv[1])
    corpus_dict = load_dict(input_file)

    for key in EXPORT_KEY_LIST:
        dict = extract_stats(corpus_dict, key)
        # print(dict)
        output_file = create_output_filename(input_file, key)
        write_output(output_file, dict)


def validate_input():
    if len(sys.argv) != 2:
        sys.exit("Usage: python visualize.py <input_file>")


def load_dict(input_file: str) -> dict:
    try:
        with open(input_file) as f:
            corpus_dict = json.load(f)
            return corpus_dict
    except FileNotFoundError:
        sys.exit("Input file does not exist")


def extract_stats(corpus_dict: dict, key: str) -> dict:
    # Create list of letter dict
    stats_dict = corpus_dict[key]

    frequency_sum = sum(list(stats_dict.values()))
    # key_with_percentage = {key: (stats_dict[key] / frequency_sum * 100) for key in stats_dict}

    key_with_percentage = {}
    for key in stats_dict.keys():
        value = round(stats_dict[key] / frequency_sum * 100, 4)
        if value >= 0.0001:
            key_with_percentage[key] = value


    sorted_letters = dict(sorted(key_with_percentage.items(), key= lambda item: item[1], reverse=True))

    return sorted_letters


def create_output_filename(input_file: str, key: str) -> str:
    file_name, _ = os.path.basename(input_file).split('.')

    output_path = os.path.dirname(input_file) + '/' + file_name + '/'
    output_file = output_path + key + '.json'
    
    os.makedirs(output_path, exist_ok=True)
    return output_file


def write_output(outfile: str, stats_dict: dict) -> None:
    with open(outfile, 'w') as f:
        f.write(json.dumps(stats_dict))
        

if __name__ == '__main__':
    main()