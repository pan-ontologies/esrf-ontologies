from typing import Set, Tuple, Generator

from .types import Technique, TechniqueMetadata
from .panet import get_techniques as get_all_techniques, get_xray_techniques, esrf_techniques


def get_technique_metadata(*aliases: Tuple[str]) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique aliases."""
    return TechniqueMetadata(techniques=set(_iter_from_aliases(*aliases)))


def get_panet_xray_techniques(*aliases: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique aliases."""
    all_techniques = get_xray_techniques()
    return all_techniques

def get_esrf_techniques(*aliases: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique aliases."""
    all_esrf_techniques = esrf_techniques()
    return all_esrf_techniques


def _iter_from_aliases(*aliases: Tuple[str]) -> Generator[Technique, None, None]:
    all_techniques = get_all_techniques()
    for alias in sorted(set(aliases)):
        try:
            alias_techniques = all_techniques[alias]
        except KeyError:
            raise KeyError(f"'{alias}' is not a known technique alias") from None
        yield from alias_techniques
