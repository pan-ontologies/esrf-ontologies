import logging
import dataclasses
from typing import List, Dict, Union, Set, MutableMapping, Tuple, Optional

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Technique:
    """Technique defined in an Ontology"""

    iri: str  # Internationalized Resource Identifier
    names: Tuple[str]  # Human readable name (first is the perferred one)
    description: str  # Human readable description

    @property
    def primary_name(self) -> str:
        return self.names[0]


@dataclasses.dataclass
class TechniqueMetadata:
    """Set of techniques with associated metadata for file (BLISS scan info)
    and data portal (ICAT dataset metafata)."""

    techniques: Set[Technique]

    def get_scan_metadata(self) -> Optional[Dict[str, Union[List[str], str]]]:
        if self.techniques:
            return self._get_nxnote()

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
        nxnote = scan_info.get("techniques")
        if nxnote is None:
            nxnote = scan_info["techniques"] = dict()
        self._fill_nxnote(nxnote)

    def _get_nxnote(self) -> Dict[str, Union[List[str], str]]:
        names = list()
        iris = list()
        for technique in sorted(
            self.techniques, key=lambda technique: technique.primary_name
        ):
            names.append(technique.primary_name)
            iris.append(technique.iri)
        return {
            "@NX_class": "NXnote",
            "names": names,
            "iris": iris,
        }

    def _fill_nxnote(self, nxnote: MutableMapping) -> None:
        names = nxnote.get("names", [])
        iris = nxnote.get("iris", [])
        techniques = dict(zip(iris, names))
        for technique in self.techniques:
            techniques[technique.iri] = technique.primary_name
        iris, names = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        nxnote.update(
            {
                "@NX_class": "NXnote",
                "names": list(names),
                "iris": list(iris),
            }
        )

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
            techniques[technique.iri] = technique.primary_name
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
            technique.iri: technique.primary_name for technique in self.techniques
        }
        return self._get_icat_metadata(techniques)

    def _get_icat_metadata(self, techniques: Dict[str, str]) -> Dict[str, str]:
        iris, definitions = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        return {"technique_pid": " ".join(iris), "definition": " ".join(definitions)}
