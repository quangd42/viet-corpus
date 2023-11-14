from extract import extract_stats
from pathlib import Path
import json

CURRENT_DIR = Path.cwd()
INPUT_DIR = CURRENT_DIR / "test"
OUTPUT_DIR = INPUT_DIR / "combined"

def test_extract_stats():
    # if not (OUTPUT_DIR / "letters.json").exists:
    #     print("No output folder")
    # if not INPUT_DIR.exists:
    #     print("No input folder")
    
    with open(OUTPUT_DIR / "letters.json") as f:
        letters = json.load(f)
    
    with open(OUTPUT_DIR / "skipgrams.json") as f:
        skipgrams = json.load(f)

    with open(INPUT_DIR / "combined.json") as f:
        corpus_dict = json.load(f)
    
    assert extract_stats(corpus_dict, "letters") == letters
    assert extract_stats(corpus_dict, "skipgrams") == skipgrams


if __name__ == "__main__":
    test_extract_stats()