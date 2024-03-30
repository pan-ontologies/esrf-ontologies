import logging
import dataclasses
from typing import List, Dict, Union, Set, MutableMapping

_logger = logging.getLogger(__name__)


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
        acronyms = list()
        names = list()
        iris = list()
        for technique in sorted(
            self.techniques, key=lambda technique: technique.acronym
        ):
            acronyms.append(technique.acronym)
            names.append(technique.name)
            iris.append(technique.iri)
        return {
            "@NX_class": "NXnote",
            "acronyms": acronyms,
            "names": names,
            "iris": iris,
        }

    def fill_dataset_metadata(self, dataset: MutableMapping) -> None:
        if not self.techniques:
            return
        # Currently handles mutable mappings by only using __getitem__ and __setitem__
        # https://gitlab.esrf.fr/bliss/bliss/-/blob/master/bliss/icat/policy.py
        try:
            definitions = dataset["definition"].split(" ")
        except KeyError:
            definitions = list()
        try:
            pids = dataset["technique_pid"].split(" ")
        except KeyError:
            pids = list()
        techniques = dict(zip(pids, definitions))
        for technique in self.techniques:
            techniques[technique.pid] = technique.acronym
        for key, value in self._get_icat_metadata(techniques).items():
            try:
                dataset[key] = value
            except KeyError:
                if key == "technique_pid":
                    _logger.warning(
                        "Skip ICAT field 'technique_pid' (requires pyicat-plus>=0.2)"
                    )
                    continue
                raise

    def get_dataset_metadata(self) -> Dict[str, str]:
        if not self.techniques:
            return dict()
        techniques = {technique.pid: technique.acronym for technique in self.techniques}
        return self._get_icat_metadata(techniques)

    def _get_icat_metadata(self, techniques: Dict[str, str]) -> Dict[str, str]:
        pids, definitions = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        return {"technique_pid": " ".join(pids), "definition": " ".join(definitions)}
