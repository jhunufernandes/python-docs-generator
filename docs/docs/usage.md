---

### Usage

#### Command Line Interface

This package provides a CLI tool to generate and manage documentation:

```bash
# Generate first python project
python_docs_generator_cli generate project --project-name my_project

# Generate complete documentation
python_docs_generator_cli generate docs

# Generate specific components
python_docs_generator_cli generate index-file
python_docs_generator_cli generate requirements
python_docs_generator_cli generate installation
python_docs_generator_cli generate docstring
python_docs_generator_cli generate mkdocs
python_docs_generator_cli generate licence
python_docs_generator_cli generate readme

# Serve documentation locally
python_docs_generator_cli serve
```

#### Programmatic Usage

You can also use the package programmatically in your Python scripts:

```python
from python_docs_generator.scripts import Generate, GenerateOptionsEnum

# Generate documentation
Generate.execute(GenerateOptionsEnum.docs)

# Generate specific component
Generate.execute(GenerateOptionsEnum.readme)
```

#### Customization

The package uses Jinja2 templates located in `src/python_docs_generator/scripts/templates/`. You can customize the output by modifying these templates to match your project's needs.
