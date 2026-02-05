<p align="center">
    <a href="https://jhunufernandes.github.io/python-docs-generator/images/python-docs-generator.svg">
        <img src="https://jhunufernandes.github.io/python-docs-generator/images/python-docs-generator.svg" alt="python-docs-generator">
    </a>
    <em>An automated documentation generator for Python projects that creates comprehensive MkDocs sites from pyproject.toml metadata and module docstrings with customizable Jinja2 templates.</em>
</p>
<p align="center">
    <a href="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/tests.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/tests.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/deploy.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/deploy.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/docs.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/python-docs-generator/actions/workflows/docs.yml/badge.svg?branch=development" alt="">
    </a>
</p>

<p align="center">
    <a href="https://jhunufernandes.github.io/python-docs-generator/license/" target="_blank">
        <img alt="License" src="https://img.shields.io/github/license/jhunufernandes/python-docs-generator">
    </a>
    <a href="https://github.com/jhunufernandes/python-docs-generator/releases" target="_blank">
        <img alt="Release" src="https://img.shields.io/github/v/release/jhunufernandes/python-docs-generator">
    </a>
</p>

**Docs**: [https://jhunufernandes.github.io/python-docs-generator/](https://jhunufernandes.github.io/python-docs-generator/)

**PyPI**: [https://pypi.org/project/python-docs-generator/](https://pypi.org/project/python-docs-generator/)

**Source**: [https://github.com/jhunufernandes/python-docs-generator/](https://github.com/jhunufernandes/python-docs-generator/)

**Board**: [https://github.com/users/jhunufernandes/projects/1/](https://github.com/users/jhunufernandes/projects/1/)

---

### Requirements

#### Prerequisites
- `python >= 3.11`
- `pip` package manager

#### Runtime Dependencies
This project requires the following Python packages with specific versions:

- `mkdocs >= 1.6.1`

- `tomli >= 2.4.0`

- `typer >= 0.21.1`

- `jinja2 >= 3.1.6`

- `cookiecutter >= 2.6.0`



#### Optional Dependencies
This project has optional dependencies that can be installed for additional features:

##### dev


##### tests

- `coverage[toml] >= 7.13.2`


##### stage

- `build >= 1.4.0`

- `coverage[toml] >= 7.13.2`



---

### Installation

#### From PyPI

```
pip install python-docs-generator
```

#### From source (as package)

```
pip install git+https://github.com/jhunufernandes/python-docs-generator.git
```

#### From source (as repo)

```
git clone https://github.com/jhunufernandes/python-docs-generator.git
cd python-docs-generator
pip install .
```
---
### Usage

#### Generate full documentation
```
python -m python_docs_generator generate docs
```

#### Generate specific artifacts
```
python -m python_docs_generator generate index-file
python -m python_docs_generator generate requirements
python -m python_docs_generator generate installation
python -m python_docs_generator generate usage
python -m python_docs_generator generate docstring
python -m python_docs_generator generate mkdocs
python -m python_docs_generator generate licence
python -m python_docs_generator generate logo
python -m python_docs_generator generate readme
```

#### Serve docs locally
```
python -m python_docs_generator serve
```

#### Create a new project from the template
```
python -m python_docs_generator generate project --project-name "My Project"
```
