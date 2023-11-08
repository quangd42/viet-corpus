"""Combine all genkey corpus stats file into one."""

import sys, json


def main():
    #TODO: Add error handling
    with open(sys.argv[1]) as f:
        corpus1 = json.load(f)
    with open(sys.argv[2]) as f:
        corpus2 = json.load(f)
    
    # init empty dict
    combined_dict = {}
    
    # letters, bigrams, trigrams, skipgrams
    for key in ['letters', 'bigrams', 'trigrams']:
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
    corpus1_toptri_list = corpus1['toptrigrams']
    corpus2_toptri_list = corpus2['toptrigrams']
    temp_toptri_list = []
    for toptri_item_2 in corpus2_toptri_list:
        # For each item in list2
        match = False
        # Loop through list1
        for toptri_item_1 in corpus1_toptri_list:
            # When an item in list1 matches item in list2:
            if toptri_item_1['Ngram'] == toptri_item_2['Ngram']:
                # Sum the count
                combined_count = toptri_item_1['Count'] + toptri_item_2['Count']
                temp_toptri_list.append({'Ngram': toptri_item_1['Ngram'], 'Count': combined_count})
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
    
    # sort the list based on key 'Count'
    corpus_combined_toptri_list = sorted(temp_toptri_list, key=lambda x: x['Count'], reverse=True)
    combined_dict['toptrigrams'] = corpus_combined_toptri_list
    # print(corpus_combined_toptri_list)


    # letters, bigrams, trigrams, skipgrams
    for key in ['skipgrams']:
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


    # TotalBigrams and Total
    for key in ['TotalBigrams', 'Total']:
        key_combined_content = corpus1[key] + corpus2[key]
        combined_dict[key] = key_combined_content

    # Combine and write
    # print(combined_dict)
    with open(sys.argv[3], 'w') as f:
        f.write(json.dumps(combined_dict))

if __name__ == "__main__":
    main()