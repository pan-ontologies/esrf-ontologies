from typing import Set, Tuple, Generator, List
from functools import lru_cache


from .types import Technique, TechniqueMetadata
from ..db import load_technniques as _load_technniques


def get_technique_metadata(*names: Tuple[str]) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique names."""
    return TechniqueMetadata(techniques=set(_iter_from_names(*names)))


def get_techniques(*names: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique names."""
    return set(_iter_from_names(*names))


@lru_cache(maxsize=1)
def get_all_techniques() -> List[Technique]:
    """Returns a list of techniques."""
    return [
        Technique(
            iri=techique["iri"],
            names=tuple(techique["names"]),
            description=techique["description"],
        )
        for ontology_name in ["ESRFET"]
        for techique in _load_technniques(ontology_name)
    ]


def _iter_from_names(*names: Tuple[str]) -> Generator[Technique, None, None]:
    techniques = get_all_techniques()
    for name in sorted(set(names)):
        for technique in techniques:
            technique_names = set(map(str.lower, technique.names))
            if name.lower() in technique_names:
                yield technique
                break
        else:
            raise KeyError(f"'{name}' is not a known technique name.")
