"""Technique information extracted from Ontologies:

- ESRFET: ESRF experimental techniques.
- PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques.
"""

import sys
import json
from typing import List, Dict, Any

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources


def load_technniques(name: str) -> List[Dict[str, Any]]:
    json_file = importlib_resources.files(__package__).joinpath(f"{name}.json")
    with open(json_file, "r") as f:
        return json.load(f)
