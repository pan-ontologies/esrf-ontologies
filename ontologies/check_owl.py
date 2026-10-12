import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set

ONTOLOGIES_DIR = Path(__file__).parent

ONTOLOGY_FILES = [
    "esrfet/ESRFET.owl",
    "esrffair/ESRFFAIR.owl",
]

OWL_NS = "http://www.w3.org/2002/07/owl#"
LABEL_PROPERTIES = {"rdfs:label", "skos:prefLabel", "skos:altLabel"}


# Dash-like characters that visually resemble the ASCII hyphen-minus.
NON_ASCII_DASHES = {
    "‐": "Hyphen",
    "‑": "Non-breaking hyphen",
    "‒": "Figure dash",
    "–": "En dash",
    "—": "Em dash",
    "―": "Horizontal bar",
    "−": "Minus sign",
    "﹘": "Small em dash",
    "－": "Fullwidth hyphen-minus",
    "᠆": "Mongolian todo soft hyphen",
}

OTHER_BAD_CHARS = {
    chr(0x00A0): "Non-breaking space",
}

BAD_CHARS = {**NON_ASCII_DASHES, **OTHER_BAD_CHARS}


def check_labels(owl_path: Path) -> List[str]:
    tree = ET.parse(owl_path)  # noqa: S314 (trusted, versioned repo file)
    errors = []
    for assertion in tree.getroot().iter(f"{{{OWL_NS}}}AnnotationAssertion"):
        prop = assertion.find(f"{{{OWL_NS}}}AnnotationProperty")
        literal = assertion.find(f"{{{OWL_NS}}}Literal")
        if prop is None or literal is None or literal.text is None:
            continue
        if prop.get("abbreviatedIRI") not in LABEL_PROPERTIES:
            continue
        errors.extend(_check_chars(literal.text, "label", owl_path))
    return errors


def check_iris(owl_path: Path) -> List[str]:
    tree = ET.parse(owl_path)  # noqa: S314 (trusted, versioned repo file)
    errors = []
    for elem in tree.getroot().iter():
        values = []
        if elem.tag.endswith("}IRI") and elem.text:
            values.append(elem.text)
        iri_attr = elem.get("IRI")
        if iri_attr:
            values.append(iri_attr)
        for value in values:
            errors.extend(_check_chars(value, "IRI", owl_path))
    return errors


def check_duplicate_declarations(owl_path: Path) -> List[str]:
    """An IRI must not be declared as more than one entity type
    (e.g. both a Class and a DataProperty)."""
    tree = ET.parse(owl_path)  # noqa: S314 (trusted, versioned repo file)
    entity_types: Dict[str, Set[str]] = defaultdict(set)
    for declaration in tree.getroot().iter(f"{{{OWL_NS}}}Declaration"):
        for entity in declaration:
            iri = entity.get("IRI") or entity.get("abbreviatedIRI")
            if iri:
                entity_types[iri].add(entity.tag.replace(f"{{{OWL_NS}}}", ""))
    return [
        f"{owl_path.name}: IRI '{iri}' is declared as multiple entity types "
        f"({', '.join(sorted(types))}); use a distinct IRI for each"
        for iri, types in entity_types.items()
        if len(types) > 1
    ]


def _check_chars(value: str, kind: str, owl_path: Path) -> List[str]:
    return [
        f"{owl_path.name}: {kind} '{value}' contains "
        f"{BAD_CHARS[char]} (U+{ord(char):04X}); "
        "use the plain ASCII equivalent instead"
        for char in set(value) & BAD_CHARS.keys()
    ]


if __name__ == "__main__":
    all_errors = []
    for owl_file in ONTOLOGY_FILES:
        owl_path = ONTOLOGIES_DIR / owl_file
        errors = (
            check_labels(owl_path)
            + check_iris(owl_path)
            + check_duplicate_declarations(owl_path)
        )
        if errors:
            all_errors.extend(errors)
        else:
            print(f"Checked: {owl_file}: OK")

    for error in all_errors:
        print(f"Error: {error}")

    if all_errors:
        sys.exit(1)
