from asyncio import run

import click

from wit_transcriber.gui.main_window import App


@click.command()
def gui() -> None:
    run(App().exec())


if __name__ == "__main__":

    @click.group()
    def cli() -> None:
        pass

    cli.add_command(gui)
    gui()
