import sys

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

from owlready2 import get_ontology
from owlready2.entity import ThingClass


def load_panet_onotology() -> ThingClass:
    owl_file = importlib_resources.files(__package__).joinpath("PaNET.owl")
    return get_ontology(owl_file.as_uri()).load()
