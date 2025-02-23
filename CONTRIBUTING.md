## Getting started

Development requirements are listed in `pyproject.toml` and can be installed with

```bash
pip install [--user] [-e] .[dev]
```

## Formatting

[black](https://black.readthedocs.io/en/stable) is used the auto-format the code.

```bash
black .
```

## Linting

[flake8](https://flake8.pycqa.org/en/latest/index.html) is used to lint the code.

```bash
flake8
```

## Ontology transpilation

Parsing the OWL files at runtime is too inefficient. Whenever we change the ontology,
this script generates data included in the python project that is more efficient
to use in production

```bash
python ontologies/parse.py
```
