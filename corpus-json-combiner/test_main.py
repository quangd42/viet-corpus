from main import combine_json
import json


def test_combine_json():
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
    assert combine_json(corpus1, corpus2) == corpus3


if __name__ == "__main__":
    test_combine_json()