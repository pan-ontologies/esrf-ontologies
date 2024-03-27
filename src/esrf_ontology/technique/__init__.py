from typing import Set, Tuple, Generator

from .types import Technique, TechniqueMetadata
from .panet import get_techniques as get_all_techniques


def get_technique_metadata(*aliases: Tuple[str]) -> TechniqueMetadata:
    """Returns an object that can generate several types of metadata
    associated to the provided technique aliases."""
    return TechniqueMetadata(techniques=set(_iter_from_aliases(*aliases)))


def get_techniques(*aliases: Tuple[str]) -> Set[Technique]:
    """Returns a set of techniques referenced by the provided technique aliases."""
    return set(_iter_from_aliases(*aliases))


def _iter_from_aliases(*aliases: Tuple[str]) -> Generator[Technique, None, None]:
    all_techniques = get_all_techniques()
    for alias in sorted(set(aliases)):
        try:
            alias_techniques = all_techniques[alias]
        except KeyError:
            raise KeyError(f"'{alias}' is not a known technique alias") from None
        yield from alias_techniques
