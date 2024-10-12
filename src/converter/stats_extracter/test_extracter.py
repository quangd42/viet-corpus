from extracter import extract_stats
from pathlib import Path
import json

CURRENT_DIR = Path.cwd()
INPUT_DIR = CURRENT_DIR / 'test'


def test_extract_stats():
    with open(INPUT_DIR / 'combined.json') as f:
        corpus_dict = json.load(f)

    with open(INPUT_DIR / 'combined_bigrams.json') as f:
        bigrams = json.load(f)

    with open(INPUT_DIR / 'combined_letters.json') as f:
        letters = json.load(f)

    with open(INPUT_DIR / 'combined_skipgrams.json') as f:
        skipgrams = json.load(f)

    with open(INPUT_DIR / 'combined_trigrams.json') as f:
        trigrams = json.load(f)

    assert extract_stats(corpus_dict, 'bigrams') == bigrams
    assert extract_stats(corpus_dict, 'letters') == letters
    assert extract_stats(corpus_dict, 'skipgrams') == skipgrams
    assert extract_stats(corpus_dict, 'trigrams') == trigrams


if __name__ == '__main__':
    test_extract_stats()
