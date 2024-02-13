import json
import sys
from pathlib import Path


EXPORT_KEY_LIST = ["letters", "bigrams", "trigrams", "skipgrams"]
# EXPORT_KEY_LIST = ['letters']


def main():
    # Load json file to dict
    input_file = validate_usage()
    corpus_dict = load_dict(input_file)

    for key in EXPORT_KEY_LIST:
        dict = extract_stats(corpus_dict, key)
        # print(dict)
        output_dir = create_output_dir(input_file)
        output_filename = create_output_filename(output_dir, key)
        write_output(output_filename, dict)


def validate_usage():
    if len(sys.argv) != 2:
        sys.exit("Usage: python extract.py <input_file>")
    return str(sys.argv[1])


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

    sorted_letters = dict(
        sorted(key_with_percentage.items(), key=lambda item: item[1], reverse=True)
    )

    return sorted_letters


def create_output_dir(input_file: str) -> Path:
    input_path = Path(input_file)
    file_name, _ = input_path.name.split(".")

    output_dir = input_path.parent / file_name
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return output_dir


def create_output_filename(output_dir: Path, key: str) -> Path:
    output_filename = f"{key}.json"
    output_path = output_dir / output_filename
    return output_path


def write_output(outfile: Path, stats_dict: dict) -> None:
    with open(outfile, "w") as f:
        f.write(json.dumps(stats_dict))


if __name__ == "__main__":
    main()
