import re
import sys
from pathlib import Path

ONTOLOGIES_DIR = Path(__file__).parent

ONTOLOGY_FILES = [
    "esrfet/ESRFET.owl",
]

version_pattern = re.compile(r"^v\d+\.\d+\.\d+$")


def check_version_format(owl_path: Path) -> str:
    from owlready2 import get_ontology

    onto = get_ontology(str(owl_path)).load()
    version = onto.metadata.versionInfo.first()

    if version is None:
        raise ValueError(f"{owl_path}: missing owl:versionInfo annotation")
    if not version_pattern.match(version):
        raise ValueError(
            f"{owl_path}: version '{version}' does not match expected format 'v<major>.<minor>.<patch>'"
        )
    return version


if __name__ == "__main__":
    errors = []
    for owl_path in ONTOLOGY_FILES:
        full_path = ONTOLOGIES_DIR / owl_path
        try:
            version = check_version_format(full_path)
            print(f"Checked: {owl_path}: {version}")
        except ValueError as e:
            print(f"Error {e}")
            errors.append(owl_path)

    if errors:
        sys.exit(1)
