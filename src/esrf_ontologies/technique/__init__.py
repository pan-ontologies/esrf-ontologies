from functools import lru_cache
from typing import Generator
from typing import List
from typing import Set
from typing import Tuple

from ..db import load_techniques as _load_techniques
from .types import BLISS_SCANINFO_CATEGORY  # noqa F401
from .types import Technique
from .types import TechniqueMetadata


def get_technique_metadata(*identifiers: Tuple[str]) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique names or IRIs."""
    return TechniqueMetadata(techniques=set(_iter_from_identifiers(*identifiers)))


def get_techniques(*identifiers: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique names or IRIs."""
    return set(_iter_from_identifiers(*identifiers))


def get_ontology_version(metadata: TechniqueMetadata) -> str:
    return next(iter(metadata.techniques)).ontology_version


def get_ontology_version_number(metadata: TechniqueMetadata) -> str:
    return get_ontology_version(metadata).lstrip("v")


@lru_cache(maxsize=1)
def get_all_techniques() -> List[Technique]:
    """Returns a list of techniques."""
    return [
        Technique(
            iri=technique["iri"],
            names=tuple(technique["names"]),
            description=technique["description"],
            ontology_version=technique["ontology_version"],
        )
        for ontology_name in ["ESRFET"]
        for technique in _load_techniques(ontology_name)
    ]


def _iter_from_identifiers(*identifiers: str) -> Generator[Technique, None, None]:
    techniques = get_all_techniques()
    for identifier in sorted(set(identifiers)):
        identifier_lower = identifier.lower()
        for technique in techniques:
            technique_names = set(map(str.lower, technique.names))
            if identifier_lower in technique_names or identifier == technique.iri:
                yield technique
                break
        else:
            raise KeyError(f"'{identifier}' is not a known technique name or IRI.")
