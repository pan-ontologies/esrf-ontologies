"""PaNET: taxonomy and thesaurus of photon and neutron (PaN) experimental techniques
"""

from typing import Tuple, Mapping
from functools import lru_cache
from types import MappingProxyType
from owlready2 import default_world

from .types import Technique
from ..ontology import load_panet_ontology, load_esrf_ontology


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


def get_xray_techniques():
    """Returns all techniques associated with x-ray probe"""
    ontology = load_esrf_ontology()
    print(ontology)
    return resultBindings(ontology, 'closeParents')



def resultBindings(ontology, sparqlQuery, classId = 'x-ray probe' ):
    print("resultBindings: ", ontology, sparqlQuery, classId)
    query = sparql_queries[sparqlQuery](classId, prefix)
    print("query", query)

    graph = default_world.as_rdflib_graph()
    print("graph", graph)
    result = list(graph.query_owlready(query))
    print(result)
    result_list = [{"parent": "#" + item[0], "label": "#" + str(item[1])} for item in result]
    print(result_list)
    return result_list


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
    "closeParents": lambda classId, prefix: f"""
        {prefix}
        SELECT ?parent
        WHERE {{
            ontology:'{classId}' rdfs:subClassOf ?parent .
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
    """
}