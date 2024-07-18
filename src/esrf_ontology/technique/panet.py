"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""
import pprint
from typing import Tuple, Mapping
from functools import lru_cache
from types import MappingProxyType
from owlready2 import default_world, get_ontology

from .types import Technique
from ..ontology import load_panet_ontology, load_esrf_ontology, use_robot
import json
from collections import defaultdict
import sys
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

    # Function to recursively find all subclasses of a given class
    def get_all_subclasses(cls):
        subclasses = set(cls.subclasses())
        for subclass in cls.subclasses():
            subclasses.update(get_all_subclasses(subclass))
        return subclasses

    xray_probe_class = onto.search_one(iri="http://purl.org/pan-science/PaNET/PaNET01012")

    all_subclasses = get_all_subclasses(xray_probe_class)

    return all_subclasses


def get_xray_techniques():
    """Returns all techniques associated with x-ray probe"""
    ontology = load_esrf_ontology()
    print(ontology)
    return resultBindings(ontology, "xrayTechniques")

def get_esrfPanet_techniques():
    """
    Returns all esrf techniques with their PaNET equivalent if exist
    Return: [{esrf_IRI, esrf_label, esrf_prefLabel, panet_IRI, panet_label}]
    """
    # TODO: if the file is empty load and query the ontology to populate it.
    # file_path = '/home/koumouts/code/esrf-ontology/src/esrf_ontology/ontology/esrf_techniques.json'
    # with open(file_path, 'r') as file:
    #     data = json.load(file)
    # techniques_sparql = data['techniques_sparql']
    # print(techniques_sparql)
    ontology = load_esrf_ontology()
    return resultBindings(ontology, "esrfPanetTechniques")


def resultBindings(ontology, sparqlQuery, classId="x-ray probe"):
    print("resultBindings: ", ontology, sparqlQuery, classId)
    query = sparql_queries[sparqlQuery](classId, prefix)
    print("query", query)

    techniques = list(default_world.sparql(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX : <http://purl.org/pan-science/PaNET/PaNET.owl#>
        PREFIX esrf: <http://www.semanticweb.org/koumouts/ontologies/2024/3/esrf_ontology#>

        SELECT ?subClass ?label ?prefLabel ?eqClass
        WHERE {{ 
            ?subClass rdfs:subClassOf esrf:experimental_technique
            OPTIONAL { ?subClass owl:equivalentClass ?eqClass }
            OPTIONAL {{?subClass rdfs:label ?label}}
            OPTIONAL {{?subClass skos:prefLabel ?prefLabel}}
            FILTER (?subClass != owl:Nothing && ?subClass != esrf:experimental_technique)
        }}
    """
    ))

    for tech in techniques:
        tech[0] = str(tech[0])
        tech[3] = str(tech[3])

    # Dictionary to store unique entries
    unique_entries = defaultdict(lambda: {"esrf_id": "", "esrf_label": "", "esrf_prefLabels": [], "definition": [], "eqClass": []})
    pprint.pprint(techniques)
    # Populate the dictionary
    for entry in techniques:
        unique_entries[entry[0]]["esrf_id"] = entry[0]
        unique_entries[entry[0]]["esrf_label"] = entry[1]
        if entry[2] not in unique_entries[entry[0]]["esrf_prefLabels"]:
            unique_entries[entry[0]]["esrf_prefLabels"].append(entry[2])
        if entry[3] not in unique_entries[entry[0]]["eqClass"] and "esrf-ontology." in entry[3]:
            unique_entries[entry[0]]["definition"].append(entry[3])
        if entry[3] not in unique_entries[entry[0]]["eqClass"] and "esrf-ontology." not in entry[3]:
            unique_entries[entry[0]]["eqClass"].append(entry[3])

    # Convert dictionary back to a list of dictionaries
    result = list(unique_entries.values())

    # Define file path
    file_path = importlib_resources.files(__package__).joinpath('../ontology/esrf_techniques.json')

    # Save to JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {file_path}")
    return techniques


prefix = "PREFIX ontology: <http://www.semanticweb.org/koumouts/ontologies/2023/8/esrf-ontology#>"


sparql_queries = {
    "closeChildren": lambda classId, prefix: f"""
        {prefix}
        SELECT ?child ?label
        WHERE {{
            ?child rdfs:subClassOf ontology:{classId} .
                OPTIONAL {{ ?child rdfs:label ?label }}
        }}
    """,
    "esrfPanetTechniques": lambda classId, prefix: f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX : <http://purl.org/pan-science/PaNET/PaNET.owl#>
        PREFIX esrf: <http://www.semanticweb.org/koumouts/ontologies/2024/3/esrf_ontology#>

        SELECT ?subClass ?label ?prefLabel ?eqClass
        WHERE {{ 
            ?subClass rdfs:subClassOf esrf:experimental_technique
            OPTIONAL {{?subclass owl:equivalentClass ?eqClass}}
            OPTIONAL {{?subClass rdfs:label ?label}}
            OPTIONAL {{?subClass skos:prefLabel ?prefLabel}}
            FILTER (?subClass != owl:Nothing && ?subClass != esrf:experimental_technique)
        }}
    """,
    "xrayTechniques": lambda classId, prefix: f"""
        {prefix}
        SELECT ?child
        WHERE {{
            ?child rdfs:subClassOf <http://purl.org/pan-science/PaNET/PaNET01012> .
        }}
    """,
    "objectProperties": lambda classId, prefix: f"""
        {prefix}
        SELECT ?objectProperty ?targetClass
        WHERE {{
            ?objectProperty a owl:ObjectProperty ;
                    rdfs:domain ontology:{classId} ;
                    rdfs:range ?targetClass .
        }}
    """,
    "upperClasses": lambda _, prefix: f"""
        {prefix}
        SELECT DISTINCT ?label ?class
        WHERE {{
        ?class a owl:Class ;
                rdfs:label ?label .
        FILTER (
            EXISTS {{ ?class rdfs:subClassOf owl:Thing . }} ||
            NOT EXISTS {{ ?class rdfs:subClassOf ?parent . }}
        )
        }}
    """,
}
