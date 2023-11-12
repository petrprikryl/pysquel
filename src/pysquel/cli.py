from pathlib import Path
from typing import Annotated

import typer

from pysquel.linter import lint_path


app = typer.Typer()


@app.command()
def cli(
    path: Annotated[
        Path,
        typer.Argument(
            exists=True,
        ),
    ],
):
    raise typer.Exit(0 if lint_path(path) else 1)


if __name__ == "__main__":
    app()
