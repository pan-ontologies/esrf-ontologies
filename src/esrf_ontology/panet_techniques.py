import os
from functools import lru_cache
from owlready2 import get_ontology
from . import techniques


@lru_cache(maxsize=1)
def get_techniques_panet():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    ontology_path = os.path.join(current_directory, "ontology/PaNET.owl")
    panet_ontology = get_ontology("file://" + ontology_path).load()
    abbreviations_info = {}
    for cls in panet_ontology.classes():
        if cls.altLabel:
            for altLabel in cls.altLabel:
                abbreviations = [
                    word
                    for word in altLabel.split()
                    if word.isupper() and len(word) >= 2
                ]
                for abbreviation in abbreviations:
                    if abbreviation not in abbreviations_info:
                        abbreviations_info[abbreviation] = {
                            "acronym": abbreviation,
                            "name": cls.label[0],
                            "panetid": int(cls.iri[-5:]),
                        }

    sorted_abbreviations_info = {
        k: abbreviations_info[k] for k in sorted(abbreviations_info)
    }
    return {
        alias: techniques.Technique(**info)
        for alias, info in sorted_abbreviations_info.items()
    }
