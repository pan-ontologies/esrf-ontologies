## Getting started

Development requirements are listed in `pyproject.toml` and can be installed with

```bash
pip install [--user] [-e] .[dev]
```

## Formatting and linting

[ruff](https://docs.astral.sh/ruff/) is used to auto-format and lint the code.

```bash
ruff format .
ruff check .
```

## Pre-commit hooks

[pre-commit](https://pre-commit.com/) runs ruff and validation checks.

Before committing, perform syntax and validation checks with:

```bash
pre-commit run --all-files
```

To run this automatically on every commit, install the Git hook:

```bash
pre-commit install
```

## Ontology transpilation

Parsing the OWL files at runtime is too inefficient. Whenever we change the ontology,
this script generates data included in the python project that is more efficient
to use in production

```bash
python ontologies/parse.py
```

## Ontology validation with ROBOT

[ROBOT](https://robot.obolibrary.org/) checks that the ontologies are in the OWL 2 DL profile, are consistent, have no unsatisfiable classes and have no inferred equivalent classes.
It also produces quality reports for information.

In GitHub, run the "ROBOT ontology validation" workflow manually from the Actions tab.
The reports are uploaded as the `robot-reports` artifact.

To run it locally, install Java 11 or higher and download the ROBOT jar file

```bash
curl -sSLf -o robot.jar https://github.com/ontodev/robot/releases/download/v1.9.8/robot.jar
python ontologies/check_robot.py --robot-jar robot.jar
```

Reports are written to `build/robot/`, one set per ontology:

| File | Content | Fails the check |
| --- | --- | --- |
| `<name>_profile.txt` | OWL 2 DL profile validation | yes |
| `<name>_reason.txt` | Reasoner errors: inconsistency, unsatisfiable classes, inferred equivalent classes. Empty when there are none. | yes |
| `<name>_report.html` / `<name>_report.tsv` | Quality report on what is written in the ontology (labels, comments, metadata, ...). HTML to read, TSV to process. | no |

The quality report rules are listed in `ontologies/robot/profile.txt`, with our own SPARQL rules in `ontologies/robot/queries/`.

## Install Protégé

Tool used to create and modify ontologies.

Download the latest release

```bash
repo="protegeproject/protege-distribution"
release_info=$(curl -s "https://api.github.com/repos/$repo/releases/latest")
download_url=$(echo "$release_info" | jq -r '.assets[] | select(.name | endswith ("linux.tar.gz")) | .browser_download_url')
# -> https://github.com/protegeproject/protege-distribution/releases/download/protege-5.6.3/Protege-5.6.3-linux.tar.gz

mkdir ./protege
wget -qO- "$download_url" | tar xvz -C ./protege --strip-components=1
```

Create desktop file

```bash
filename=~/.local/share/applications/protege.desktop
echo "[Desktop Entry]" > $filename
echo "Type=Application" >> $filename
echo "Terminal=true" >> $filename
echo "Name=Protégé" >> $filename
echo "Icon=$(pwd)/protege/app/Protege.icns" >> $filename
echo "Exec=$(pwd)/protege/run.sh" >> $filename
```

## Update local PaNET Ontology (ontologies/panet/PaNET.owl)

```bash
curl -L -o ontologies/panet/PaNET.owl http://purl.org/pan-science/PaNET/PaNET.owl
```

## Update local NeXus Ontology (ontologies/nexus/NeXusOntology_full_*.owl)

1. **Update NeXus Ontology submodule**  
   Update the NeXus Ontology submodule to the latest commit. This should pull the latest commit from oscars-project branch. So you now have latest owl file:
   ```bash
   git submodule update --remote --recursive NeXusOntology
   ```

2. **Copy the tracked ontology to local**  
   Copy the ontology file to the target location:
   ```bash
   cp NeXusOntology/ontology/NeXusOntology_full_*.owl ontologies/nexus/
   ```
