# TODO: merge all these small files into one, ship with genkey
# TODO: write readme.md explaining how to use

# Run telex-converter to process and get 20 txt files in telex
# Import convert_multiple_lines_to_telex, get list of 20 files as output
# Note that 20 files actually were created
# Run genkey-runner to get json files from genkey

# Run corpus-json-combiner to combine all those json files into one big file, this is the main corpus.json

# Run extracter to see relevant stats

# Delete files created by other modules

import sys
import click
from pathlib import Path

from .telex_converter import telexify as tc

MAPPING_PATH = Path(
    "./src/converter/telex_converter/new_telex_mapping-w.json"
).resolve()
DATA_PATH = Path("./data")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--limit",
    "-l",
    default=1000,
    help="Limit the number of lines processed, in case you have a very big input file",
)
@click.option(
    "--name",
    "-n",
    prompt=True,
    required=True,
    type=str,
    help="Give this text a name so you can look up its stats later.",
)
def load(filename: str, limit: int, name: str):
    """Load, convert vietnamese text and spit out key usage."""

    # Load telex mapping
    telex_mapping = tc.load_telex_mapping(MAPPING_PATH)
    if not tc.validate_telex_mapping(telex_mapping):
        sys.exit("telex mapping contains invalid info")

    telex_text_list = tc.convert_multiple_lines_to_telex(filename, telex_mapping, limit)

    output_path = DATA_PATH / name
    Path.mkdir(output_path, parents=True, exist_ok=True)
    output_count = tc.save_telex_output(telex_text_list, output_path)

    print(f"{'-' * 5}")
    if output_count == 0:
        print("No file created. Something went wrong.")
    else:
        print(
            f"{output_count} files created successfully. Output written to {output_path}"
        )


@cli.command()
def view():
    click.echo("You're viewing something")
