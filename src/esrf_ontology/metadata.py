from dataclasses import dataclass
from typing import List, Dict, Union, Set
from . import techniques


@dataclass
class TechniqueMetadata:
    techniques: Set[techniques.TechniqueModel]

    def get_scan_info(self) -> Dict[str, Dict[str, Union[List[str], str]]]:
        if not self.techniques:
            return dict()
        scan_info_acronyms = list()
        scan_info_names = list()
        scan_info_urls = list()

        scan_info = {
            "techniques": {
                "@NX_class": "NXnote",
                "acronyms": scan_info_acronyms,
                "names": scan_info_names,
                "urls": scan_info_urls,
            },
            "scan_meta_categories": ["techniques"],
        }
        for technique in sorted(
            self.techniques, key=lambda technique: technique.acronym
        ):
            scan_info_acronyms.append(technique.acronym)
            scan_info_names.append(technique.name)
            scan_info_urls.append(technique.url)
        return scan_info

    def get_dataset_techniques(self) -> List[str]:
        return sorted({technique.acronym for technique in self.techniques})


def get_technique_metadata(*aliases) -> TechniqueMetadata:
    return TechniqueMetadata(
        techniques={techniques.get_technique(alias) for alias in sorted(set(aliases))}
    )
