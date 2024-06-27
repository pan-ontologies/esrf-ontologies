"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""

from typing import Tuple, Mapping
from functools import lru_cache
from types import MappingProxyType
from owlready2 import default_world, get_ontology

from .types import Technique
from ..ontology import load_panet_ontology, load_esrf_ontology, use_robot
import json


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


def resultBindings(ontology, sparqlQuery, classId="x-ray probe"):
    print("resultBindings: ", ontology, sparqlQuery, classId)
    query = sparql_queries[sparqlQuery](classId, prefix)
    print("query", query)
    # use_robot.run_robot_reasoner()
    # graph = default_world.as_rdflib_graph()
    # print("graph", graph)
    # result = list(graph.query_owlready(query))
    techniques = list(
        default_world.sparql(
            """
           SELECT DISTINCT ?child ?label
        WHERE {
            ?child rdfs:subClassOf* <http://purl.org/pan-science/PaNET/PaNET01012> .
            OPTIONAL {?child rdfs:label ?label}
        }
    """
        )
    )
    for tech in techniques:
        tech[0] = str(tech[0])

    file_path = '/home/koumouts/code/esrf-ontology/src/esrf_ontology/ontology/xray_probe_sparql.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    techniques_sparql = data['techniques_sparql']
    # print(techniques_sparql)

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
    "xrayTechniques": lambda classId, prefix: f"""
        {prefix}
        SELECT ?child
        WHERE {{
            ?child rdfs:subClassOf* <http://purl.org/pan-science/PaNET/PaNET01012> .
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
