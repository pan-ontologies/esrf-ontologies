from functools import lru_cache
from typing import Generator
from typing import List
from typing import Optional
from typing import Set

from ..db import load_techniques as _load_techniques
from .types import BLISS_SCANINFO_CATEGORY  # noqa F401
from .types import Technique
from .types import TechniqueMetadata


def get_technique_metadata(*identifiers: str) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique names or IRIs."""
    return TechniqueMetadata(techniques=set(_iter_from_identifiers(*identifiers)))


def get_techniques(*identifiers: str) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique names or IRIs."""
    return set(_iter_from_identifiers(*identifiers))


def get_technique(identifier: str) -> Technique:
    """Returns a technique referenced by the provided technique name or IRI."""
    return next(_iter_from_identifiers(identifier))


def get_ontology_version(metadata: Optional[TechniqueMetadata] = None) -> str:
    if metadata is None:
        technique = get_technique("XRAYS")
    else:
        technique = next(iter(metadata.techniques))
    return technique.ontology_version


def get_ontology_version_number(metadata: Optional[TechniqueMetadata] = None) -> str:
    return get_ontology_version(metadata=metadata).lstrip("v")


@lru_cache(maxsize=1)
def get_all_techniques() -> List[Technique]:
    """Returns a list of techniques."""
    return [
        Technique(
            iri=technique["iri"],
            names=tuple(technique["names"]),
            description=technique["description"],
            ontology_version=technique["ontology_version"],
            versioned_iri=f'{technique["iri"].split("#")[0]}/{technique["ontology_version"]}/#{technique["iri"].split("#")[1]}',
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
            if (
                identifier_lower in technique_names
                or identifier == technique.iri
                or identifier == technique.versioned_iri
            ):
                yield technique
                break
        else:
            raise KeyError(f"'{identifier}' is not a known technique name or IRI.")
