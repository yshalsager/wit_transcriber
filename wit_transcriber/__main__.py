"""Entry Point."""
import click

from wit_transcriber.cli.app import transcribe
from wit_transcriber.gui.app import gui


@click.group()
def click_cli() -> None:
    pass


def main() -> None:
    click_cli.add_command(transcribe)
    click_cli.add_command(gui)
    click_cli()


if __name__ == "__main__":
    main()
