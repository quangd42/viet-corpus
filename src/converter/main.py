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
from pathlib import Path

import click


from .telex_converter import telexify as tc
from .genkey_runner import genkey_runner as gr

MAPPING_PATH = Path(
    "./src/converter/telex_converter/new_telex_mapping-w.json"
).resolve()
DATA_PATH = Path("./data")

GENKEY_FOLDER_PATH = Path("./src/converter/genkey_runner/genkey").resolve()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--limit",
    "-l",
    default=10000,
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

    # Check output path
    output_path = DATA_PATH / name / "tmp"
    while output_path.exists():
        is_confirmed = click.confirm(
            f"{name} is already used. Are you sure you want to overwrite?"
        )
        if not is_confirmed:
            name = click.prompt("Name")
            output_path = DATA_PATH / name / "tmp"
        else:
            break

    Path.mkdir(output_path, parents=True, exist_ok=True)

    click.echo(f"{'*' * 10}")
    output_count = tc.convert_and_save(filename, telex_mapping, limit, output_path)

    click.echo(f"{'-' * 5}")
    if output_count == 0:
        click.echo("No file created. Something went wrong.")
    else:
        click.echo(
            f"{output_count} files created successfully. Output written to {output_path}."
        )

    # Run genkey
    click.echo(f"{'*' * 10}")

    if not gr.check_genkey_exist(GENKEY_FOLDER_PATH):
        sys.exit("Cannot find genkey executable.")
    gr_file_list = gr.get_input_file_list(output_path)
    gr_output_path = gr.create_output_dir(output_path)
    gr_output_files = gr.run_genkey(gr_file_list, gr_output_path, GENKEY_FOLDER_PATH)
    click.echo(f"{'-' * 5}")
    click.echo(
        f"{len(gr_output_files) } files analyzed with genkey. Output written to {gr_output_path}."
    )
    click.echo(f"{'*' * 10}")


@cli.command()
def view():
    click.echo("You're viewing something")
