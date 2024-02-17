"""Combine all genkey corpus stats file into one."""

import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python combine.py <input_dir>")
    else:
        # Get input_path and create json file list
        input_dir = Path(sys.argv[1])
        file_list = get_json_file_list(input_dir)

        # output_dir = Path(sys.argv[2])

        combined_dict = combine_all_json(file_list)

        save_output_json(combined_dict, input_dir)


def get_json_file_list(input_dir_path: Path) -> list[Path]:
    return list(input_dir_path.glob("*.json"))


def save_output_json(combined_dict: dict, output_dir: Path) -> Path:
    # Write file to output
    file_name = "combined.json"
    output_path = output_dir / file_name
    # Make sure output directory is there
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(json.dumps(combined_dict))

    return output_path


def combine_all_json(file_list: list) -> dict:
    combined_dict = {}
    # Loop through json file list
    for input_file in file_list:
        # Load json file to dict
        try:
            with open(input_file) as f:
                corpus_dict = json.load(f)
        except FileNotFoundError:
            sys.exit("Input file does not exist")

        # Create combined_dict
        if not combined_dict:
            combined_dict = corpus_dict

        else:
            combined_dict = combine_two_json(combined_dict, corpus_dict)

    return combined_dict


def combine_two_json(corpus_dict1: dict, corpus_dict2: dict) -> dict:
    corpus1 = corpus_dict1
    corpus2 = corpus_dict2

    combined_dict = {}

    # letters, bigrams, trigrams, skipgrams
    for key in ["letters", "bigrams", "trigrams", "skipgrams"]:
        key_combined_content = corpus1[key]
        key_2 = corpus2[key]
        for sub_key in key_combined_content:
            try:
                key_combined_content[sub_key] += key_2[sub_key]
            except KeyError:
                pass
        for sub_key in key_2:
            if sub_key not in key_combined_content:
                key_combined_content[sub_key] = key_2[sub_key]
        combined_dict[key] = key_combined_content

    # toptrigrams
    corpus1_toptri_list = corpus1["toptrigrams"]
    corpus2_toptri_list = corpus2["toptrigrams"]
    temp_toptri_list = []
    for toptri_item_2 in corpus2_toptri_list:
        # For each item in list2
        match = False
        # Loop through list1
        for toptri_item_1 in corpus1_toptri_list:
            # When an item in list1 matches item in list2:
            if toptri_item_1["Ngram"] == toptri_item_2["Ngram"]:
                # Sum the count
                combined_count = toptri_item_1["Count"] + toptri_item_2["Count"]
                temp_toptri_list.append(
                    {"Ngram": toptri_item_1["Ngram"], "Count": combined_count}
                )
                # Remove the item from list1 for when getting to next item from list2
                corpus1_toptri_list.remove(toptri_item_1)
                match = True
                # Then move on to next item from list2
                break
        # If there is no match in list1 at all, that list2 item can be appended as is
        if not match:
            temp_toptri_list.append(toptri_item_2)
    # After looping through all items in list2, whatever left in list1 has no match and can be appended as is
    for toptri_item_1 in corpus1_toptri_list:
        temp_toptri_list.append(toptri_item_1)

    # Sort the list based on key 'Count'
    corpus_combined_toptri_list = sorted(
        temp_toptri_list, key=lambda x: x["Count"], reverse=True
    )
    combined_dict["toptrigrams"] = corpus_combined_toptri_list

    # TotalBigrams and Total
    for key in ["TotalBigrams", "Total"]:
        key_combined_content = corpus1[key] + corpus2[key]
        combined_dict[key] = key_combined_content

    # Combine and write
    order = [
        "letters",
        "bigrams",
        "trigrams",
        "toptrigrams",
        "skipgrams",
        "TotalBigrams",
        "Total",
    ]
    ordered_dict = {key: combined_dict[key] for key in order}
    # print(ordered_dict)

    # If all is well return combined json as dict
    return ordered_dict


if __name__ == "__main__":
    main()
