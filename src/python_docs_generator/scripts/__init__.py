"""The module that contains the CLI commands.

Classes:
    Command: The commands that can be executed by the CLI.
    Generate: The class that executes the commands based on the provided arguments.
"""

from datetime import datetime, timezone
from enum import Enum
from importlib import import_module
from pathlib import Path

from cookiecutter.main import cookiecutter
from typer import echo
from yaml import dump, safe_load

from .commons import (
    DOCS_PATH,
    ROOT_PATH,
    DocsGenerator,
    get_imports_from_module,
    create_directory,
    read_pyproject,
    recursive_writer,
    to_snake_case,
)


class GenerateOptionsEnum(str, Enum):
    """The options that can be executed by the CLI.

    Options:
        docs
        docstring
        index-file
        installation
        licence
        logo
        mkdocs
        project
        readme
        requirements
        usage
    """

    docs = "docs"
    docstring = "docstring"
    index_file = "index-file"
    installation = "installation"
    licence = "licence"
    logo = "logo"
    mkdocs = "mkdocs"
    project = "project"
    readme = "readme"
    requirements = "requirements"
    usage = "usage"


class Generate:
    """The class that executes the options based on the provided arguments.

    Methods:
        execute: Executes the option based on the provided arguments.
    """
    @staticmethod
    def execute(option: GenerateOptionsEnum, project_name: str | None = None) -> None:
        """Executes the option based on the provided arguments."""
        match option:
            case GenerateOptionsEnum.docs:
                Generate.execute(GenerateOptionsEnum.licence)

                Generate.execute(GenerateOptionsEnum.index_file)
                Generate.execute(GenerateOptionsEnum.requirements)
                Generate.execute(GenerateOptionsEnum.installation)
                Generate.execute(GenerateOptionsEnum.usage)
                Generate.execute(GenerateOptionsEnum.readme)

                Generate.execute(GenerateOptionsEnum.docstring)
                Generate.execute(GenerateOptionsEnum.mkdocs)

            case GenerateOptionsEnum.docstring:
                project_slug = to_snake_case(str(ROOT_PATH.absolute()).split("/")[-1])
                echo(f"Generating docs for {project_slug}")

                project_module = import_module(project_slug)
                heading_level = 3
                imports_from_module = get_imports_from_module(project_module, heading_level)

                api_path = DOCS_PATH / "api"
                create_directory(api_path)

                echo("Clearing API Reference folder")
                for doc in api_path.glob("*"):
                    doc.unlink()

                for doc in imports_from_module:
                    to_render = recursive_writer(doc)
                    with open(doc.path, "w") as doc_file:
                        doc_file.write(to_render)

                echo(f"Generated docs for {project_slug}")

            case GenerateOptionsEnum.index_file:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                docs_generator.render("index.md")

            case GenerateOptionsEnum.installation:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                docs_generator.render("installation.md")

            case GenerateOptionsEnum.licence:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                year = datetime.now(timezone.utc).year
                docs_generator.render("license.md", year=year)
                docs_generator.render("license.md", ROOT_PATH, "LICENSE", year=year)

            case GenerateOptionsEnum.logo:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                assert project_name is not None, "Project name is required for project"
                path = DOCS_PATH / "images"
                docs_generator.render("logo.svg", path, f"{project_name}.svg")

            case GenerateOptionsEnum.mkdocs:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                Generate.execute(GenerateOptionsEnum.docstring)

                # prerender mkdocs.yml
                docs_generator.render("mkdocs.yml", ROOT_PATH / "docs")

                # append API references to mkdocs.yml
                echo("Generating API Reference")

                echo("Reading temp mkdocs")
                with open(ROOT_PATH / "docs" / "mkdocs.yml") as mkdocs_file:
                    mkdocs_dict = safe_load(mkdocs_file.read())

                echo("Getting references")
                api_references = sorted([i.name for i in Path.iterdir(DOCS_PATH / "api")])

                echo("Rendering mkdocs_dict with the data")
                for section in mkdocs_dict["nav"]:
                    if "API Reference" in section:
                        section["API Reference"] = [
                            {"_".join(i.split("_")[1:]).rsplit(".", 1)[0]: f"api/{i}"} for i in api_references
                        ]

                echo("Writing mkdocs")
                with open(ROOT_PATH / "docs" / "mkdocs.yml", "w") as mkdocs_file:
                    dump(mkdocs_dict, mkdocs_file)

                echo("Generated API Reference")

            case GenerateOptionsEnum.project:
                assert project_name is not None, "Project name is required for project"

                echo(f"Generating project with name: {project_name}")

                echo("Cloning template")
                cookiecutter(  # type: ignore
                    "gh:jhunufernandes/python-package-template",
                    no_input=True,
                    extra_context={
                        "project_name": project_name,
                        "project_slug": to_snake_case(project_name),
                    },
                    overwrite_if_exists=True,
                )

                Generate.execute(GenerateOptionsEnum.logo, project_name)
                Generate.execute(GenerateOptionsEnum.licence)

            case GenerateOptionsEnum.readme:
                Generate.execute(GenerateOptionsEnum.index_file)
                Generate.execute(GenerateOptionsEnum.requirements)
                Generate.execute(GenerateOptionsEnum.installation)
                Generate.execute(GenerateOptionsEnum.usage)

                echo(f"Writing {ROOT_PATH}/README.md with:")
                with open(ROOT_PATH / "README.md", "w") as f:
                    for file_to_concatenate in [
                        DOCS_PATH / f"{i}.md" for i in ["index", "requirements", "installation", "usage"]
                    ]:
                        echo(f" - {file_to_concatenate.name}")
                        with open(file_to_concatenate) as _f:
                            f.write(_f.read())
                            f.write("\n")

                echo(f"Generated {ROOT_PATH}/README.md")

            case GenerateOptionsEnum.requirements:
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                docs_generator.render("requirements.md")

            case GenerateOptionsEnum.usage:
                usage_file = DOCS_PATH / "usage.md"
                if usage_file.exists():
                    echo(f"usage.md already exists at {DOCS_PATH}, skipping generation")
                    return
                
                pyproject_content = read_pyproject()
                docs_generator = DocsGenerator(pyproject_content, project_name=project_name)

                docs_generator.render("usage.md")
