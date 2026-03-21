from functools import lru_cache
from typing import Generator
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from ..db import load_techniques as _load_techniques
from .types import BLISS_SCANINFO_CATEGORY  # noqa F401
from .types import Technique
from .types import TechniqueMetadata


def get_technique_metadata(*names: Tuple[str]) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique names."""
    return TechniqueMetadata(techniques=set(_iter_from_names(*names)))


def get_techniques(*names: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique names."""
    return set(_iter_from_names(*names))


def get_technique(name: str) -> Technique:
    """Returns a technique referenced by the provided technique name."""
    return next(_iter_from_names(name))


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
        )
        for ontology_name in ["ESRFET"]
        for technique in _load_techniques(ontology_name)
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
