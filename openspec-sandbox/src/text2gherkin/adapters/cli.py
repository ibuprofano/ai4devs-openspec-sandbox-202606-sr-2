import sys
from pathlib import Path
from typing import Optional

import typer

from text2gherkin.engine import convert

app = typer.Typer()


@app.callback()
def main() -> None:
    """text2gherkin: convert free-form text describing user actions into Gherkin."""


@app.command(name="convert")
def convert_command(
    input_file: Optional[Path] = typer.Argument(
        None, help="Input text file. Reads from stdin if omitted."
    ),
    output: Optional[Path] = typer.Option(
        None, "-o", "--output", help="Output file. Writes to stdout if omitted."
    ),
) -> None:
    """Convert free-form text describing user actions into a Gherkin feature file."""
    if input_file is not None:
        text = input_file.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    try:
        result = convert(text)
    except Exception as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if output is not None:
        output.write_text(result, encoding="utf-8")
    else:
        typer.echo(result, nl=False)
