import sys
from owlready2 import sync_reasoner

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

from owlready2 import get_ontology
from owlready2.entity import ThingClass


def load_panet_ontology() -> ThingClass:
    owl_file = importlib_resources.files(__package__).joinpath("PaNET.owl")
    return get_ontology(owl_file.as_uri()).load()


def load_esrf_ontology() -> ThingClass:
    # owl_file = importlib_resources.files(__package__).joinpath("esrf_ontology.owl")
    owl_file = "/home/koumouts/code/esrf-ontology/src/esrf_ontology/ontology/robot_esrf_ontology.owl"
    # ontology = get_ontology(owl_file.as_uri()).load()
    ontology = get_ontology(owl_file).load()
    with ontology:
        sync_reasoner()
    # ontology.save()
    print(ontology)
    return ontology
