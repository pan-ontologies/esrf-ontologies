import dataclasses
from typing import List, Dict, Union, Set, MutableMapping


@dataclasses.dataclass(frozen=True)
class Technique:
    pid: str  # Persistent IDentifier within the ESRF Ontology
    iri: str  # Internationalized Resource Identifier
    name: str  # Human readable name
    acronym: str  # Human readable acronym without spaces


@dataclasses.dataclass
class TechniqueMetadata:
    techniques: Set[Technique]

    def get_scan_info(self) -> Dict[str, Dict[str, Union[List[str], str]]]:
        if not self.techniques:
            return dict()
        return {
            "techniques": self._get_nxnote(),
            "scan_meta_categories": ["techniques"],
        }

    def fill_scan_info(self, scan_info: MutableMapping) -> None:
        if not self.techniques:
            return
        scan_meta_categories = scan_info.setdefault("scan_meta_categories", list())
        if "techniques" not in scan_meta_categories:
            scan_meta_categories.append("techniques")
        scan_info["techniques"] = self._get_nxnote()

    def _get_nxnote(self) -> Dict[str, Union[List[str], str]]:
        scan_info_acronyms = list()
        scan_info_names = list()
        scan_info_iris = list()
        techniques = {
            "@NX_class": "NXnote",
            "acronyms": scan_info_acronyms,
            "names": scan_info_names,
            "iris": scan_info_iris,
        }
        for technique in sorted(
            self.techniques, key=lambda technique: technique.acronym
        ):
            scan_info_acronyms.append(technique.acronym)
            scan_info_names.append(technique.name)
            scan_info_iris.append(technique.iri)
        return techniques

    def fill_dataset_metadata(self, dataset: MutableMapping) -> None:
        if not self.techniques:
            return
        # Currently handles mutable mappings by only using __getitem__ and __setitem__
        # https://gitlab.esrf.fr/bliss/bliss/-/blob/master/bliss/icat/policy.py
        try:
            values = dataset["definition"].split(" ")
        except KeyError:
            values = list()
        try:
            keys = dataset["technique_pid"].split(" ")
        except KeyError:
            keys = list()
        techniques = dict(zip(keys, values))
        for technique in self.techniques:
            techniques[technique.pid] = technique.acronym
        for key, value in self._get_icat_metadata(techniques).items():
            dataset[key] = value

    def get_dataset_metadata(self) -> Dict[str, str]:
        if not self.techniques:
            return dict()
        techniques = {technique.pid: technique.acronym for technique in self.techniques}
        return self._get_icat_metadata(techniques)

    def _get_icat_metadata(self, techniques: Dict[str, str]) -> Dict[str, str]:
        keys, values = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        return {"technique_pid": " ".join(keys), "definition": " ".join(values)}
