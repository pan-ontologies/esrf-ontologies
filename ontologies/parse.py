import os
import json
from typing import Set, List, Dict, Any
from tabulate import tabulate

from owlready2 import get_ontology
from owlready2 import sync_reasoner
from owlready2.entity import ThingClass
from owlready2.namespace import Ontology


from esrf_ontologies.technique import get_all_techniques


def load_ontology(*args) -> Ontology:
    owl_file = os.path.join(os.path.dirname(__file__), *args)
    return get_ontology(owl_file).load()


def get_all_subclasses(cls: ThingClass) -> Set[ThingClass]:
    subclasses = set(cls.subclasses())
    for subclass in cls.subclasses():
        subclasses.update(get_all_subclasses(subclass))
    return subclasses


def get_subclass_tree(cls, path: str = None) -> Dict[str, ThingClass]:
    if not path:
        path = ""
    clsdict = dict()

    for subclass in cls.subclasses():
        sub_path = f"{path}/{subclass.name}"
        subclsdict = get_subclass_tree(subclass, sub_path)
        if subclsdict:
            clsdict.update(subclsdict)
        else:
            clsdict[sub_path] = subclass

    return clsdict


def get_names(cls: ThingClass) -> List[str]:
    names = []
    for name in cls.label:
        name = name.strip()
        if name not in names:
            names.append(name)
    for name in cls.prefLabel:
        name = name.strip()
        if name not in names:
            names.append(name)
    for name in cls.altLabel:
        name = name.strip()
        if name not in names:
            names.append(name)
    return names


def save_techniques(name: str, techniques: List[Dict[str, Any]]):
    json_file = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "..", "src", "esrf_ontologies", "db", name
        )
    )
    techniques = sorted(techniques, key=lambda technique: technique["names"][0])
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(techniques, f, indent=2)


def get_esrfet_techniques():
    ontology = load_ontology("esrfet", "ESRFET.owl")

    with ontology:
        sync_reasoner()

    experimental_technique_base = ontology.search_one(
        iri="http://www.semanticweb.org/koumouts/ontologies/2024/3/esrf_ontology#experimental_technique"
    )

    techniques = []

    for cls in get_all_subclasses(experimental_technique_base):
        names = get_names(cls)
        description = "\n".join(cls.comment)
        techniques.append(
            {"iri": cls.iri.strip(), "names": names, "description": description}
        )

    save_techniques("ESRFET.json", techniques)


def get_esrfet_building_blocks():

    ontology = load_ontology("esrfet", "ESRFET.owl")

    building_blocks = ontology.search_one(
        iri="http://www.semanticweb.org/koumouts/ontologies/2024/3/esrf_ontology#technique_property"
    )

    subclasses = get_subclass_tree(building_blocks)
    for name in subclasses:
        print(name)


def get_panet_techniques():
    ontology = load_ontology("panet", "PaNET.owl")

    xray_probe_class = ontology.search_one(
        iri="http://purl.org/pan-science/PaNET/PaNET01012"
    )

    techniques = []

    for cls in get_all_subclasses(xray_probe_class):
        names = get_names(cls)
        names = sorted(names, key=len)
        description = "\n".join(cls.comment)
        techniques.append({"iri": cls.iri, "names": names, "description": description})

    save_techniques("PaNET.json", techniques)


def generate_docs():
    docdir = os.path.join(os.path.dirname(__file__), "..", "doc")

    headers = ["Name", "Alternative names", "Description"]
    table = [
        [
            f"`{technique.names[0]} <{technique.iri}>`_",  # noqa W604
            ", ".join(technique.names[1:]),
            technique.description,
        ]
        for technique in sorted(
            get_all_techniques(), key=lambda technique: technique.names
        )
    ]

    with open(os.path.join(docdir, "techniques.rst"), "w", encoding="utf-8") as f:
        f.write(".. _techniques:\n\n")
        f.write("Techniques\n==========\n\n")
        f.write(
            "The **name** and **alternative names** can be used in :meth:`esrf_ontology.technique.get_technique_metadata`.\n\n"
        )
        f.write(tabulate(table, headers, tablefmt="rst"))


if __name__ == "__main__":
    # get_esrfet_building_blocks()
    get_esrfet_techniques()
    get_panet_techniques()
    generate_docs()
