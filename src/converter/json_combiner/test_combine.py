from combine import combine_two_json, combine_all_json
from pathlib import Path
import os


corpus1 = {
    "letters": {"a": 1, "b": 2, "f": 5, "d": 10},
    "bigrams": {"ab": 1},
    "trigrams": {"the": 1},
    "toptrigrams": [{"Ngram": "you", "Count": 5}, {"Ngram": "the", "Count": 1}, {"Ngram": "right", "Count": 10}],
    "skipgrams": {"dz": 209.2},
    "TotalBigrams": 10,
    "Total": 15
}
corpus2 = {
    "letters": {"a": 2, "b": 5, "c": 3, "f": 1},
    "bigrams": {"ab": 1},
    "trigrams": {"the": 1},
    "toptrigrams": [{"Ngram": "you", "Count": 3}, {"Ngram": "the", "Count": 2}, {"Ngram": "man", "Count": 1}],
    "skipgrams": {"dz": 209.2},
    "TotalBigrams": 30,
    "Total": 50
}
corpus3 = {
    "letters": {
        "a": 3,
        "b": 7,
        "f": 6,
        "d": 10,
        "c": 3
    },
    "bigrams": {
        "ab": 2
    },
    "trigrams": {
        "the": 2
    },
    "toptrigrams": [
        {
            "Ngram": "right",
            "Count": 10
        },
        {
            "Ngram": "you",
            "Count": 8
        },
        {
            "Ngram": "the",
            "Count": 3
        },
        {
            "Ngram": "man",
            "Count": 1
        }
    ],
    "skipgrams": {
        "dz": 418.4
    },
    "TotalBigrams": 40,
    "Total": 65
}
corpus4 = {
    "letters": {
        "a": 6,
        "b": 14,
        "f": 12,
        "d": 20,
        "c": 6
    },
    "bigrams": {
        "ab": 4
    },
    "trigrams": {
        "the": 4
    },
    "toptrigrams": [
        {
            "Ngram": "right",
            "Count": 20
        },
        {
            "Ngram": "you",
            "Count": 16
        },
        {
            "Ngram": "the",
            "Count": 6
        },
        {
            "Ngram": "man",
            "Count": 2
        }
    ],
    "skipgrams": {
        "dz": 836.8
    },
    "TotalBigrams": 80,
    "Total": 130
}


def test_combine_two_json():
    assert combine_two_json(corpus1, corpus2) == corpus3


def test_combine_all_json():
    input_dir = Path(os.getcwd() + "/test")
    file_list = list(input_dir.glob("*.json"))

    assert combine_all_json(file_list) == corpus4


if __name__ == "__main__":
    test_combine_two_json()
    test_combine_all_json()