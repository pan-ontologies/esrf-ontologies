"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""

import pprint
from typing import Tuple, Mapping
from functools import lru_cache
from types import MappingProxyType
from owlready2 import default_world, get_ontology

from .types import Technique
from ..ontology import (
    load_panetReasoned_ontology,
    load_panet_ontology,
    load_esrf_ontology,
)
import json
from collections import defaultdict
import sys
from owlready2 import sync_reasoner_pellet
from .sparql_queries import sparql_queries

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources


@lru_cache(maxsize=1)
def get_techniques() -> Mapping[str, Tuple[Technique]]:
    """Returns a map from technique alias to associated PaNET techniques."""
    techniques = {}
    for cls in load_panet_ontology().classes():
        for altLabel in cls.altLabel:
            acronyms = [
                word for word in altLabel.split() if word.isupper() and len(word) >= 2
            ]
            for acronym in acronyms:
                if acronym not in techniques:
                    alias_techniques = (
                        Technique(
                            pid=cls.name,
                            iri=cls.iri,
                            name=cls.label[0],
                            acronym=acronym,
                        ),
                    )
                    techniques[acronym] = alias_techniques
    return MappingProxyType(techniques)


def get_xray_techniques_parsing():
    onto = get_ontology("http://purl.org/pan-science/PaNET/PaNET.owl").load()

    # Recursively find all subclasses of a given class
    def get_all_subclasses(cls):
        subclasses = set(cls.subclasses())
        for subclass in cls.subclasses():
            subclasses.update(get_all_subclasses(subclass))
        return subclasses

    xray_probe_class = onto.search_one(
        iri="http://purl.org/pan-science/PaNET/PaNET01012"
    )
    all_subclasses = get_all_subclasses(xray_probe_class)
    return all_subclasses


def get_techniques_from_file(owl_file):
    try:
        with open(owl_file, "r") as file:
            data = json.load(owl_file)
            if data:
                return data
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return None


def queryResults(ontology, sparqlQuery, classId):
    prefix = "PREFIX esrf: <http://www.semanticweb.org/koumouts/ontologies/2024/3/esrf_ontology#>"
    queries = sparql_queries(classId, prefix)
    query = queries[sparqlQuery](classId, prefix)
    return list(default_world.sparql(query))


def get_xray_techniques():
    """Returns all techniques associated with x-ray probe"""
    ontology = load_panetReasoned_ontology()
    xray_techniques = queryResults(
        ontology, "xrayTechniques", "<http://purl.org/pan-science/PaNET/PaNET01012>"
    )
    pprint.pprint(xray_techniques)
    return xray_techniques


def esrf_techniques(refresh_tecniques=False, reasoned_ontology=False):
    """
    Returns all esrf techniques with their PaNET equivalent if exist
    Return: [{esrf_id, esrf_label, esrf_prefLabel, definition, eqClass}]
    """
    if not refresh_tecniques:
        esrf_techniques_file = importlib_resources.files(__package__).joinpath(
            "esrf_techniques.json"
        )
        techniques = get_techniques_from_file(esrf_techniques_file)
        if techniques:
            return techniques

    ontology = load_esrf_ontology()

    if reasoned_ontology:
        with ontology:
            # seems that the reasoners (native or pellet) dont work to have all subclasses of "x-ray probe"
            # it seems to work to get the equivalent classes for esrf+PaNET ontology.
            sync_reasoner_pellet()

    techniques = queryResults(ontology, "esrfTechniques", "esrf:experimental_technique")
    for tech in techniques:
        tech[0] = str(tech[0])
        tech[3] = str(tech[3])

    # Dictionary to store unique entries
    unique_entries = defaultdict(
        lambda: {
            "esrf_id": "",
            "esrf_label": "",
            "esrf_prefLabels": [],
            "definition": [],
            "eqClass": [],
        }
    )
    pprint.pprint(techniques)

    for entry in techniques:
        unique_entries[entry[0]]["esrf_id"] = entry[0]
        unique_entries[entry[0]]["esrf_label"] = entry[1]
        if entry[2] not in unique_entries[entry[0]]["esrf_prefLabels"]:
            unique_entries[entry[0]]["esrf_prefLabels"].append(entry[2])
        if (
            entry[3] not in unique_entries[entry[0]]["eqClass"]
            and "esrf-ontology." in entry[3]
        ):
            unique_entries[entry[0]]["definition"].append(entry[3])
        if (
            entry[3] not in unique_entries[entry[0]]["eqClass"]
            and "esrf-ontology." not in entry[3]
        ):
            unique_entries[entry[0]]["eqClass"].append(entry[3])

    # Convert dictionary back to a list of dictionaries
    result = list(unique_entries.values())

    # Define file path
    file_path = importlib_resources.files(__package__).joinpath(
        "../ontology/esrf_techniques.json"
    )

    # Save to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {file_path}")
    return techniques
