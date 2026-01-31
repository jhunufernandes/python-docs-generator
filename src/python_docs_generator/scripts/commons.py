from pathlib import Path
from re import sub
from types import FunctionType, ModuleType
from typing import Any, Literal

from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass
from tomli import loads
from typer import echo

ROOT_PATH = Path()
DOCS_PATH = ROOT_PATH / "docs" / "docs"

Templates = Environment(loader=FileSystemLoader(str(Path(__file__).parent / "templates")))
TypesMapping = Literal["module", "function", "class"]


def read_pyproject(path: Path | None = None) -> dict[str, Any]:
    """Reads the pyproject.toml file and returns its content as a dictionary.

    Args:
        path (Path): The path to the pyproject.toml file. Defaults to None.

    Returns:
        dict[str, Any]: The content of the pyproject.toml file as a dictionary
    """
    path = ROOT_PATH / "pyproject.toml" or path
    with open(path) as pyproject_file:
        return loads(pyproject_file.read())


def to_snake_case(string: str) -> str:
    """Converts a given string to snake case.

    Args:
        string (str): The string to be converted.

    Returns:
        str: The converted string in snake case.
    """
    s1 = sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    s2 = sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return sub(r"-", "_", s2).lower()


def create_directory(path: Path) -> None:
    """Creates a directory if it does not exist.

    Args:
        path (Path): The path of the directory to create.
    """
    echo(f"Creating directory at {path}")
    path.mkdir(parents=True, exist_ok=True)
    echo(f"Directory created at {path}")


def _get_import_type_mapping(_import: Any) -> TypesMapping | None:
    import_type: Any = type(_import)  # type: ignore
    if import_type == ModuleType:
        return "module"
    if import_type == FunctionType:
        return "function"
    if isinstance(_import, type):
        return "class"


def _get_docstring(obj: Any) -> str:
    doc = getattr(obj, "__doc__", None)
    return doc or ""


@dataclass
class Doc:
    """Represents documentation metadata for an object.

    Attributes:
        name (str): The name of the object.
        path (Path): The output file path for the documentation.
        docstring (str): The docstring or description.
        level (int): The Markdown heading level.
        sub (list["Doc"]): List of Doc objects for sub-objects.
    """

    name: str
    path: Path
    docstring: str
    level: int
    sub: list["Doc"]


def recursive_writer(doc: Doc) -> str:
    """Recursively write documentation for a Doc object and its sub-objects.

    Args:
        doc (Doc): The Doc object to write.

    Returns:
        str: The rendered Markdown string for this Doc and its children.
    """
    echo(f"Writing docstring from import: {doc.name}")
    template = Templates.get_template("docstring.md")  # type: ignore
    return template.render(  # type: ignore
        name=doc.name,
        docstring=doc.docstring,
        heading_level=doc.level * "#",
        sub="\n".join([recursive_writer(s) for s in doc.sub]),
    )


def get_imports_from_module(module: ModuleType, level: int) -> list[Doc]:
    """Recursively extract documentation metadata from a module's __all__ exports.

    Args:
        module (ModuleType): The module to inspect.
        level (int): The Markdown heading level.

    Returns:
        list[Doc]: A list of Doc objects representing the module's exports.
    """
    echo(f"Getting imports from {module.__name__} module")

    docs: list[Doc] = []
    for i in getattr(module, "__all__", []):
        echo(f"Getting metadata from {i} import")

        _import = getattr(module, i)
        name = _import.__name__
        filename = _import.__name__
        sub = []
        import_type = _get_import_type_mapping(_import) or ""
        if import_type == "module":
            name = _import.__spec__.name
            sub = get_imports_from_module(_import, level + 1)
            filename = to_snake_case(i)

        docs.append(
            Doc(
                name=name,
                path=DOCS_PATH / "api" / f"{import_type}_{filename}.md",
                docstring=_get_docstring(_import),
                level=level,
                sub=sub,
            ),
        )
    return docs


class DocsGenerator:
    """Base class for documentation generators."""

    def __init__(
        self,
        pyproject_content: dict[str, Any],
        organization_name: str | None = None,
        project_name: str | None = None,
    ) -> None:
        """Initialize the documentation generator.

        Args:
            pyproject_content (dict[str, Any]): The content of pyproject.toml.
            organization_name (str | None): The name of the organization. Defaults to None.
            project_name (str | None): The name of the project. Defaults to None.
        """
        self.pyproject_content = pyproject_content
        self.organization_name = organization_name or "jhunufernandes"
        self.project_name = project_name

    def render(
        self,
        template_file: str,
        destiny_path: Path | None = None,
        new_file: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Generate documentation file.

        This method renders a template file with the provided data and writes it to the specified path.

        Args:
            file (str): The name of the file to generate (e.g., "index.md").
            path (Path | None): The path where the file will be saved. Defaults to DOCS_PATH.
            new_file (str | None): If provided, the content will be written to this new file instead of `template_file`.
            **kwargs (Any): Additional keyword arguments to pass to the template rendering.
        """
        echo(f"Generating {template_file}")

        echo("Rendering the template with the data")
        template = Templates.get_template(template_file)  # type: ignore
        content: str = template.render(  # type: ignore
            **self.pyproject_content,
            organization_name=self.organization_name,
            project_name=self.project_name,
            **kwargs or {},
        )

        destiny_file = new_file or template_file
        destiny_path = destiny_path or DOCS_PATH
        destiny_file_path = destiny_path / destiny_file

        create_directory(destiny_path or DOCS_PATH)
        echo(f"Writing {destiny_file_path}")
        with open(destiny_file_path, "w") as f:
            f.write(content)  # type: ignore

        echo(f"Generated {destiny_file_path}")
