"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""

from typing import Tuple, Mapping
from functools import lru_cache
from types import MappingProxyType

from .types import Technique
from ..ontology import load_panet_onotology


@lru_cache(maxsize=1)
def get_techniques() -> Mapping[str, Tuple[Technique]]:
    """Returns a map from technique alias to associated PaNET techniques."""
    techniques = {}
    for cls in load_panet_onotology().classes():
        for altLabel in cls.altLabel:
            acronyms = [
                word for word in altLabel.split() if word.isupper() and len(word) >= 2
            ]
            for acronym in acronyms:
                if acronym not in techniques:
                    alias_techniques = (
                        Technique(
                            pid=cls.name,
                            iri=cls.iri,
                            name=cls.label[0],
                            acronym=acronym,
                        ),
                    )
                    techniques[acronym] = alias_techniques
    return MappingProxyType(techniques)
