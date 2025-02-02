import os

from owlready2 import get_ontology
from owlready2.entity import ThingClass


def load_ontology(*args) -> ThingClass:
    owl_file = os.path.join(os.path.dirname(__file__), *args)
    return get_ontology(owl_file).load()


def get_techniques():
    """Returns a map from technique alias to associated PaNET techniques."""
    ontology = load_ontology("panet", "PaNET.owl")
    for cls in ontology.classes():
        print(cls.name, cls.iri, cls.label, cls.altLabel)

    return
    ontology = load_ontology("esrfet", "ESRFET.owl")
    for cls in ontology.classes():
        print(cls.name, cls.iri, cls.label, cls.altLabel)



if __name__ == "__main__":
    get_techniques()