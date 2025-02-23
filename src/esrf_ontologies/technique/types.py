import logging
import dataclasses
from typing import List, Dict, Union, Set, MutableMapping, Tuple

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Technique:
    """Technique defined in an Ontology"""

    iri: str  # Internationalized Resource Identifier
    names: Tuple[str]  # Human readable name (first is the perferred one)
    description: str  # Human readable description


@dataclasses.dataclass
class TechniqueMetadata:
    """Set of techniques with associated metadata for file (BLISS scan info)
    and data portal (ICAT dataset metafata)."""

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
        names = list()
        iris = list()
        for technique in sorted(
            self.techniques, key=lambda technique: technique.names[0]
        ):
            names.append(technique.names[0])
            iris.append(technique.iri)
        return {
            "@NX_class": "NXnote",
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
            techniques[technique.iri] = technique.names[0]
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
        techniques = {
            technique.iri: technique.names[0] for technique in self.techniques
        }
        return self._get_icat_metadata(techniques)

    def _get_icat_metadata(self, techniques: Dict[str, str]) -> Dict[str, str]:
        iris, definitions = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        return {"technique_pid": " ".join(iris), "definition": " ".join(definitions)}
