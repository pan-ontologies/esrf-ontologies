prefixes = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX : <http://purl.org/pan-science/PaNET/PaNET.owl#>
    """


def sparql_queries(classId, prefix):
    return {
        "closeChildren": lambda classId, prefix: f"""
        {prefixes}
        {prefix}
        SELECT ?child ?label
        WHERE {{
            ?child rdfs:subClassOf ontology:{classId} .
                OPTIONAL {{ ?child rdfs:label ?label }}
        }}
    """,
        "esrfTechniques": lambda classId, prefix: f"""
        {prefixes}
        {prefix}
        SELECT ?subClass ?label ?prefLabel ?eqClass
        WHERE {{ 
            ?subClass rdfs:subClassOf esrf:experimental_technique
            OPTIONAL {{ ?subClass owl:equivalentClass ?eqClass }}
            OPTIONAL {{?subClass rdfs:label ?label}}
            OPTIONAL {{?subClass skos:prefLabel ?prefLabel}}
            FILTER (?subClass != owl:Nothing && ?subClass != esrf:experimental_technique)
        }}
    """,
        "xrayTechniques": lambda classId, prefix: f"""
        {prefixes}
        {prefix}
        SELECT ?subClass ?label
        WHERE {{
            ?child rdfs:subClassOf <http://purl.org/pan-science/PaNET/PaNET01012> 
            OPTIONAL {{ ?subClass rdfs:label ?label}}
        }}
    """,
        "objectProperties": lambda classId, prefix: f"""
        {prefixes}        
        {prefix}
        SELECT ?objectProperty ?targetClass
        WHERE {{
            ?objectProperty a owl:ObjectProperty ;
                    rdfs:domain ontology:{classId} ;
                    rdfs:range ?targetClass .
        }}
    """,
        "upperClasses": lambda _, prefix: f"""
        {prefixes}
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
