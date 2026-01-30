"""CLI and main application entry points.

Provides Typer CLI commands for generating, updating, and serving documentation and projects.
"""

from mkdocs.commands.serve import serve
from typer import Typer, echo

from .scripts import Generate
from .scripts.commons import ROOT_PATH

app = Typer()
state = {}


@app.callback()
def callback() -> None:
    pass


@app.command()
def deploy() -> None:
    pass


@app.command()
def generate(option: Generate.GenerateOptionsEnum, project_name: str | None = None) -> None:
    Generate.execute(option, project_name)


@app.command()
def serve() -> None:
    echo("Serving documentation...")

    config_file_path = str(ROOT_PATH / "docs" / "mkdocs.yml")
    serve(config_file_path)  # type: ignore
