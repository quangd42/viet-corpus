"""Combine all genkey corpus stats file into one."""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: python combine.py <input_dir>')
    else:
        # Get input_path and create json file list
        input_dir = Path(sys.argv[1])
        file_list = get_json_file_list(input_dir)

        combined_dict = combine_all_json(file_list)

        save_output_json(combined_dict, input_dir)


def get_json_file_list(input_dir_path: Path) -> list[Path]:
    return list(input_dir_path.glob('*.json'))


def save_output_json(combined_dict: dict, output_dir: Path) -> Path:
    # Write file to output
    file_name = 'combined.json'
    output_path = output_dir / file_name
    # Make sure output directory is there
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(json.dumps(combined_dict))

    return output_path


def combine_all_json(file_list: list[Path]) -> dict:
    combined_dict = {}
    # Loop through json file list
    for input_file in file_list:
        # Load json file to dict
        try:
            with open(input_file) as f:
                corpus_dict = json.load(f)
        except FileNotFoundError:
            sys.exit('Input file does not exist')

        # Create combined_dict
        if combined_dict == {}:
            combined_dict = corpus_dict
        else:
            try:
                combined_dict = combine_two_json(combined_dict, corpus_dict)
            except KeyError:
                sys.exit(f'Invalid input file format: {input_file}.')

    return combined_dict


def combine_two_json(corpus1: dict, corpus2: dict) -> dict:
    combined_dict = {}

    # letters, bigrams, trigrams, skipgrams
    for key in ['letters', 'bigrams', 'trigrams', 'skipgrams']:
        key__combined_content = corpus1[key].copy()
        key__corpus2 = corpus2[key].copy()
        for sub_key in list(key__combined_content.keys()):
            try:
                key__combined_content[sub_key] += key__corpus2[sub_key]
                del key__corpus2[sub_key]
            except KeyError:
                pass
        for sub_key in key__corpus2.keys():
            key__combined_content[sub_key] = key__corpus2[sub_key]
        combined_dict[key] = key__combined_content

    # toptrigrams
    try:
        corpus1_toptri_list = corpus1['TopTrigrams']
    except KeyError:
        corpus1_toptri_list = corpus1['toptrigrams']

    try:
        corpus2_toptri_list = corpus2['TopTrigrams']
    except KeyError:
        corpus2_toptri_list = corpus2['toptrigrams']

    corpus2_toptri_dict = {item['Ngram']: item['Count'] for item in corpus2_toptri_list}
    for toptri_item_1 in corpus1_toptri_list:
        # If an item in list 1 exist in list 2, add combine it and del from list 2
        if (ngram := toptri_item_1['Ngram']) in corpus2_toptri_dict:
            toptri_item_1['Count'] += corpus2_toptri_dict[ngram]
            del corpus2_toptri_dict[ngram]
    # After looping through all items in list1, whatever left in list2 has no match and can be added as is
    corpus2_toptri_list = [
        {'Ngram': key, 'Count': value} for (key, value) in corpus2_toptri_dict.items()
    ]
    corpus1_toptri_list.extend(corpus2_toptri_list)

    # Sort the list based on key 'Count'
    corpus_combined_toptri_list = sorted(
        corpus1_toptri_list, key=lambda x: x['Count'], reverse=True
    )
    combined_dict['TopTrigrams'] = corpus_combined_toptri_list

    # TotalBigrams and Total
    for key in ['TotalBigrams', 'Total']:
        key__combined_content = corpus1[key] + corpus2[key]
        combined_dict[key] = key__combined_content

    # Combine and write
    ordered_dict = {
        'letters': combined_dict['letters'],
        'bigrams': combined_dict['bigrams'],
        'trigrams': combined_dict['trigrams'],
        'TopTrigrams': combined_dict['TopTrigrams'],
        'skipgrams': combined_dict['skipgrams'],
        'TotalBigrams': combined_dict['TotalBigrams'],
        'Total': combined_dict['Total'],
    }

    # If all is well return combined json as dict
    return ordered_dict


if __name__ == '__main__':
    main()
