def generate_telex_mapping(vowel_clusters):
    mapping = {}

    for cluster in vowel_clusters:
        main = ''
        modifier = ''
        diacritic_mark = ''

        if cluster[0] in ['a', 'á', 'ă', 'ắ', 'â', 'ấ']:
            main = 'a'

        if cluster[0] in ['á', 'ắ', 'ấ']:
            diacritic_mark = 's'

        if cluster[0] in ['ă', 'ắ', 'ơ']:
            modifier = 'w'

        value = main + modifier + diacritic_mark
        mapping[cluster] = value

    return mapping

# Provide the list of Vietnamese vowel clusters with diacritic marks
vowel_clusters = ['a', 'á', 'ă', 'ắ', 'â', 'ấ', 'o', 'ô', 'ơ', 'ư']

# Generate telex mapping based on the provided vowel clusters
telex_mapping = generate_telex_mapping(vowel_clusters)
print(telex_mapping)
