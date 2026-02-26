import re
from pathlib import Path

import pytest
from owlready2 import get_ontology


def find_repo_root(marker: str = "pyproject.toml") -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Could not find repo root (no {marker} found)")


ONTOLOGIES_DIR = find_repo_root() / "ontologies"

ONTOLOGY_FILES = [
    "esrfet/ESRFET.owl",
]

version_pattern = re.compile(r"^v\d+\.\d+\.\d+$")


@pytest.mark.parametrize("owl_path", ONTOLOGY_FILES)
def test_version_format(owl_path):
    full_path = ONTOLOGIES_DIR / owl_path
    onto = get_ontology(str(full_path)).load()
    version = onto.metadata.versionInfo.first()

    assert version is not None, f"{owl_path}: missing owl:versionInfo annotation"
    assert version_pattern.match(
        version
    ), f"{owl_path}: version '{version}' does not match expected format 'v<major>.<minor>.<patch>'"
