import sys
from owlready2 import sync_reasoner_pellet

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

from owlready2 import get_ontology
from owlready2.entity import ThingClass


def load_panetReasoned_ontology() -> ThingClass:
    owl_file = importlib_resources.files(__package__).joinpath("PaNET_reasoned.owl")
    return get_ontology(owl_file.as_uri()).load()


def load_panet_ontology() -> ThingClass:
    owl_file = importlib_resources.files(__package__).joinpath("PaNET.owl")
    return get_ontology(owl_file.as_uri()).load()


def load_esrf_ontology() -> ThingClass:
    owl_file = importlib_resources.files(__package__).joinpath("esrf-ontology.owl")
    ontology = get_ontology(str(owl_file)).load()
    return ontology
