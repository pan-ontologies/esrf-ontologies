import sys
from owlready2 import sync_reasoner_pellet

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
    owl_file = "/home/koumouts/code/esrf-ontology/src/esrf_ontology/ontology/PaNET_reasoned.owl"
    # ontology = get_ontology(owl_file.as_uri()).load()
    ontology = get_ontology(owl_file).load()
    with ontology:
        # seems that the reasoners (native or pellet) dont work to have all subclasses of "x-ray probe"
        sync_reasoner_pellet()
    # ontology.save()
    print(ontology)
    return ontology
