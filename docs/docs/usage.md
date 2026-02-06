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