"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""

from typing import Dict
from functools import lru_cache

from .types import Technique
from ..ontology import load_panet_onotology


@lru_cache(maxsize=1)
def get_techniques() -> Dict[str, Technique]:
    techniques = {}
    for cls in load_panet_onotology().classes():
        for altLabel in cls.altLabel:
            acronyms = [
                word for word in altLabel.split() if word.isupper() and len(word) >= 2
            ]
            for acronym in acronyms:
                if acronym not in techniques:
                    techniques[acronym] = Technique(
                        id=cls.name, iri=cls.iri, name=cls.label[0], acronym=acronym
                    )
    return techniques
