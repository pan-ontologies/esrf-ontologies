import os
import json
from typing import Set, List, Dict, Any
from tabulate import tabulate

from owlready2 import get_ontology
from owlready2 import Thing
from owlready2.namespace import Ontology

from esrf_ontology.technique import get_all_techniques


def load_ontology(*args) -> Ontology:
    owl_file = os.path.join(os.path.dirname(__file__), *args)
    return get_ontology(owl_file).load()


def get_all_subclasses(cls) -> Set[Thing]:
    subclasses = set(cls.subclasses())
    for subclass in cls.subclasses():
        subclasses.update(get_all_subclasses(subclass))
    return subclasses


def get_names(cls: Thing) -> List[str]:
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
    json_file = os.path.join(
        os.path.dirname(__file__), "..", "src", "esrf_ontology", "db", name
    )
    techniques = sorted(techniques, key=lambda technique: technique["names"][0])
    with open(json_file, "w") as f:
        json.dump(techniques, f, indent=2)


def get_esrfet_techniques():
    ontology = load_ontology("esrfet", "ESRFET.owl")

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
            f"`{technique.names[0]} <{technique.iri}>`_",
            ", ".join(technique.names[1:]),
            technique.description,
        ]
        for technique in sorted(
            get_all_techniques(), key=lambda technique: technique.names
        )
    ]

    with open(os.path.join(docdir, "techniques.rst"), "w") as f:
        f.write(".. _techniques:\n\n")
        f.write("Techniques\n==========\n\n")
        f.write(
            "The **name** and **alternative names** can be used in :meth:`esrf_ontology.technique.get_technique_metadata`.\n\n"
        )
        f.write(tabulate(table, headers, tablefmt="rst"))


if __name__ == "__main__":
    get_esrfet_techniques()
    get_panet_techniques()
    generate_docs()
