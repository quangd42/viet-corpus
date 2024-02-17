import click


def create_section_separator() -> None:
    click.echo(f"{'-' * 10}")


def create_sub_section_separator() -> None:
    click.echo(f"{'.' * 5}")
