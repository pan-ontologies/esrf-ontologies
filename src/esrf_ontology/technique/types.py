import dataclasses
from typing import List, Dict, Union, Set


@dataclasses.dataclass(frozen=True)
class Technique:
    id: str  # Machine readable ID, unique within the ESRF Ontology
    iri: str  # Internationalized Resource Identifier
    name: str  # Human readable name
    acronym: str  # Human readable acronym without spaces


@dataclasses.dataclass
class TechniqueMetadata:
    techniques: Set[Technique]

    def get_scan_info(self) -> Dict[str, Dict[str, Union[List[str], str]]]:
        if not self.techniques:
            return dict()
        scan_info_acronyms = list()
        scan_info_names = list()
        scan_info_iris = list()

        scan_info = {
            "techniques": {
                "@NX_class": "NXnote",
                "acronyms": scan_info_acronyms,
                "names": scan_info_names,
                "iris": scan_info_iris,
            },
            "scan_meta_categories": ["techniques"],
        }
        for technique in sorted(
            self.techniques, key=lambda technique: technique.acronym
        ):
            scan_info_acronyms.append(technique.acronym)
            scan_info_names.append(technique.name)
            scan_info_iris.append(technique.iri)
        return scan_info

    def get_dataset_techniques(self) -> List[str]:
        return sorted({technique.acronym for technique in self.techniques})
