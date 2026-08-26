import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from dashes import NON_ASCII_DASHES

ONTOLOGIES_DIR = Path(__file__).parent

ONTOLOGY_FILES = [
    "esrfet/ESRFET.owl",
    "esrffair/ESRFFAIR.owl",
]

OWL_NS = "http://www.w3.org/2002/07/owl#"
LABEL_PROPERTIES = {"rdfs:label", "skos:prefLabel", "skos:altLabel"}


def check_labels(owl_path: Path) -> list:
    tree = ET.parse(owl_path)  # noqa: S314 (trusted, versioned repo file)
    errors = []
    for assertion in tree.getroot().iter(f"{{{OWL_NS}}}AnnotationAssertion"):
        prop = assertion.find(f"{{{OWL_NS}}}AnnotationProperty")
        literal = assertion.find(f"{{{OWL_NS}}}Literal")
        if prop is None or literal is None or literal.text is None:
            continue
        if prop.get("abbreviatedIRI") not in LABEL_PROPERTIES:
            continue
        for char in set(literal.text) & NON_ASCII_DASHES.keys():
            errors.append(
                f"{owl_path.name}: label '{literal.text}' contains "
                f"{NON_ASCII_DASHES[char]} (U+{ord(char):04X}); "
                "use the ASCII hyphen-minus '-' instead"
            )
    return errors


if __name__ == "__main__":
    all_errors = []
    for owl_file in ONTOLOGY_FILES:
        errors = check_labels(ONTOLOGIES_DIR / owl_file)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"Checked: {owl_file}: OK")

    for error in all_errors:
        print(f"Error: {error}")

    if all_errors:
        sys.exit(1)
