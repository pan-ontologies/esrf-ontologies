import sys
from pathlib import Path
from typing import List

from owlready2 import ThingClass
from owlready2 import get_ontology
from owlready2 import sync_reasoner
from parse import get_all_subclasses

ONTOLOGIES_DIR = Path(__file__).parent

ESRFET_PREFIX = "https://w3id.org/PaN/ESRFET"


def find_equivalent_techniques(owl_path: Path) -> List[List[str]]:
    """Return the groups of experimental techniques the reasoner infers to be equivalent."""
    ontology = get_ontology(str(owl_path)).load()
    with ontology:
        sync_reasoner(debug=0)

    base = ontology.search_one(iri=f"{ESRFET_PREFIX}#experimental_technique")

    groups = set()
    for cls in get_all_subclasses(base):
        equivalents = {eq for eq in cls.equivalent_to if isinstance(eq, ThingClass)}
        if equivalents:
            groups.add(frozenset(eq.name for eq in equivalents | {cls}))
    return sorted(sorted(group) for group in groups)


if __name__ == "__main__":
    owl_file = "esrfet/ESRFET.owl"
    groups = find_equivalent_techniques(ONTOLOGIES_DIR / owl_file)

    for group in groups:
        print(f"Error: {owl_file}: equivalent techniques: {', '.join(group)}")

    if groups:
        sys.exit(1)
    print(f"Checked: {owl_file}: OK")
