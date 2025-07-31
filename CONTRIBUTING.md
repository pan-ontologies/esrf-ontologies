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
## Updating local NeXus Ontology (ontologies/nexus/NeXusOntology_full_*.owl)

1. **Update NeXus Ontology submodule**  
   Update the NeXus Ontology submodule to the latest commit. This should pull the the latest commit from oscars-project branch. So you now have latest owl file:
   ```bash
   git submodule update --remote --recursive NeXusOntology
   ```

2. **Copy the tracked ontology to local**  
   Copy the ontology file to the target location:
   ```bash
   cp NeXusOntology/ontology/NeXusOntology_full_*.owl ontologies/nexus/
   ```
