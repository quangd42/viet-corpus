import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import click

from .genkey_runner import genkey_runner as gr
from .json_combiner import combine as jc
from .stats_extracter import extracter as se
from .telex_converter import telexify as tc
from .util import create_section_separator, create_sub_section_separator

MAPPING_PATH = Path(
    "./src/converter/telex_converter/new_telex_mapping-w.json"
).resolve()
DATA_PATH = Path("./data")

GENKEY_FOLDER_PATH = Path("./src/converter/genkey_runner/genkey").resolve()


@click.group()
def cli():
    """Thin wrapper around genkey to analyze Vietnamese text.

    To see help for each command use: converter COMMAND --help"""
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--limit",
    "-l",
    default=10000,
    help="Limit the number of lines processed, in case you have a very big input file.",
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
    output_path = DATA_PATH / name
    while output_path.exists():
        is_confirmed = click.confirm(
            f"{name} is already used. Are you sure you want to overwrite?"
        )
        if not is_confirmed:
            name = click.prompt("Name")
            output_path = DATA_PATH / name
        else:
            break

    # Put all tmp files in one folder for easy clean up
    tmp_dir_path = output_path / "tmp"
    Path.mkdir(tmp_dir_path, parents=True, exist_ok=True)

    create_section_separator()
    click.echo("Converting texts into telex input...")
    output_count = tc.convert_and_save(filename, telex_mapping, limit, tmp_dir_path)

    create_sub_section_separator()
    if output_count == 0:
        click.echo("No file created. Something went wrong.")
    else:
        click.echo(
            f"{output_count} files created successfully. Output written to {tmp_dir_path}."
        )

    # Run genkey
    create_section_separator()
    click.echo("Analyzing telex input files with genkey...")

    if not gr.check_genkey_exist(GENKEY_FOLDER_PATH):
        sys.exit("Cannot find genkey executable.")
    gr_file_list = gr.get_input_file_list(tmp_dir_path)
    gr_output_path = gr.create_output_dir(tmp_dir_path)
    gr_output_files = gr.run_genkey(gr_file_list, gr_output_path, GENKEY_FOLDER_PATH)
    create_sub_section_separator()
    click.echo(
        f"{len(gr_output_files) } files analyzed with genkey. Output written to {gr_output_path}."
    )
    create_section_separator()

    # Combine result
    json_file_list = jc.get_json_file_list(gr_output_path)
    if len(json_file_list) == 0:
        sys.exit("No json file found. Something went wrong.")
    combined_corpus_dict = jc.combine_all_json(json_file_list)
    combined_filename = jc.save_output_json(combined_corpus_dict, gr_output_path)
    final_json_path = output_path / f"{name}.json"

    # Copy result to the main dir and rename
    shutil.copyfile(combined_filename, final_json_path)

    click.echo(f"Corpus json combined into {final_json_path}.")
    create_section_separator()

    # Extract stats
    corpus_dict = se.load_dict(final_json_path)
    for key in se.EXPORT_KEY_LIST:
        dict = se.extract_stats(corpus_dict, key)
        se_output_filename = se.create_output_filename(final_json_path, key)
        se.save_output(se_output_filename, dict)

    click.echo(f"Corpus json data extracted. Results saved into {output_path}.")
    create_section_separator()

    # Clean up tmp dir
    shutil.rmtree(tmp_dir_path)
    click.echo("Tmp data cleaned up. Enjoy!")


@cli.command()
@click.argument(
    "name",
    type=str,
)
@click.option(
    "--stat_name", "-st", prompt=True, required=True, help="Stat name to view", type=str
)
@click.option("--limit", "-l", default=20, help="Number of top ngrams to view.")
def view(name: str, stat_name: str, limit: int):
    """View stats of a loaded Vietnamese corpus `name`.

    Valid stat names are 'letters', 'bigrams', 'trigrams', 'skipgrams'."""

    if stat_name not in se.EXPORT_KEY_LIST:
        sys.exit(f"Invalid argument. Valid arguments are {se.EXPORT_KEY_LIST}.")

    # Check name
    input_path = DATA_PATH / name
    if not input_path.exists():
        sys.exit(f"Stats for {name} does not exist.")

    input_file = input_path / f"{name}_{stat_name}.json"
    try:
        with open(input_file) as f:
            dict = json.load(f)
            count = 0
            for key in dict:
                count += 1
                if count > limit:
                    break
                click.echo(f"'{key}': {dict[key]}")

    except FileNotFoundError:
        sys.exit("Stat file does not exit.")


@cli.command()
def list():
    """List names of loaded Vietnamese corpus."""

    names = [d.name for d in DATA_PATH.iterdir() if d.is_dir()]

    for name in names:
        click.echo(name)


@cli.command()
@click.argument("pathname")
@click.option(
    "--name",
    "-n",
    type=str,
    help="Combined json filename.",
)
def combine(pathname: str, name: str | None):
    """Combine corpus json and output one with aggregated stats."""

    input_path = Path(pathname)
    if not input_path.exists() or not input_path.is_dir():
        sys.exit("Provided path does not exist or is not a directory.")
    json_file_list = jc.get_json_file_list(input_path)
    if len(json_file_list) == 0:
        sys.exit("No json file found. Something went wrong.")
    combined_corpus_dict = jc.combine_all_json(json_file_list)
    combined_filename = jc.save_output_json(combined_corpus_dict, input_path)
    if name:
        final_json_path = input_path / f"{name}.json"
    else:
        today = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_json_path = input_path / f"combined_{today}.json"
    output_path = combined_filename.rename(final_json_path)

    click.echo(f"Corpus json data combined. Results saved into {output_path}.")


# TODO: refactor using Click Exception?
