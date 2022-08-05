from asyncio import run
from pathlib import Path

import click

from wit_transcriber import CONFIG_FILE
from wit_transcriber.api_client.client import WitAiAPI


@click.command()
@click.option(
    "-i",
    "--input",
    "file_path",
    type=Path,
    help="Path of media file to be transcribed.",
    required=True,
)
@click.option("-o", "--output", type=Path, help="Path of output file.")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=Path,
    help="Path of config file.",
    default=CONFIG_FILE,
)
@click.option(
    "-x", "--connections", type=int, help="Number of API connections limit.", default=5
)
@click.option("-l", "--lang", type=str, help="Language to use.", default="ar")
@click.option("-v", "--verbose", type=bool, help="Print API responses.", default=False)
def transcribe(
    file_path: Path,
    output: Path,
    connections: int,
    config_file: Path,
    verbose: bool = False,
    lang: str = "ar",
) -> None:
    run(run_transcribe(file_path, output, connections, config_file, verbose, lang))


async def run_transcribe(
    file_path: Path,
    output: Path,
    connections: int,
    config_file: Path,
    verbose: bool,
    lang: str,
) -> None:
    """Speech to text using Wit.ai"""
    if not file_path.exists():
        raise RuntimeError("Input file doesn't exist! Exiting!")
    if not config_file.exists():
        raise RuntimeError("Config was not found! Exiting!")
    output_file = output if output else Path(f"{file_path.stem}.txt")

    api_client = WitAiAPI(lang, connections, config_file, verbose=verbose)
    if not api_client.has_api_key():
        raise RuntimeError("Language API key was not found! Exiting!")
    await api_client.transcribe(file_path)
    Path(output_file).write_text(api_client.text, encoding="utf-8")
    print("Done Successfully!")


if __name__ == "__main__":

    @click.group()
    def cli() -> None:
        pass

    cli.add_command(transcribe)
    cli()
