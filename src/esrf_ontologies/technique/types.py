import dataclasses
import logging
from typing import Dict
from typing import List
from typing import MutableMapping
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Technique:
    """Technique defined in an Ontology"""

    iri: str  # Internationalized Resource Identifier
    names: Tuple[str]  # Human readable name (first is the perferred one)
    description: str  # Human readable description
    ontology_version: str  # Ontology version extracted from OWL

    @property
    def primary_name(self) -> str:
        return self.names[0]

    @property
    def versioned_iri(self) -> str:
        """Return versioned IRI derived from stable IRI and ontology version"""
        base, fragment = self.iri.split("#", 1)
        return f"{base}/{self.ontology_version}/#{fragment}"


BLISS_SCANINFO_CATEGORY = ""
_NEXUS_IDENTIFIER_PREFIX = "identifier_technique_"


@dataclasses.dataclass
class TechniqueMetadata:
    """Set of techniques with associated metadata for file (BLISS scan info)
    and data portal (ICAT dataset metafata)."""

    techniques: Set[Technique]

    def get_scan_metadata(
        self,
    ) -> Optional[Dict[str, Union[List[str], Dict[str, str]]]]:
        if self.techniques:
            return self._get_nxentry_children()

    def get_scan_info(self) -> Dict[str, Union[List[str], Dict[str, str]]]:
        if not self.techniques:
            return dict()
        return {
            BLISS_SCANINFO_CATEGORY: self._get_nxentry_children(),
            "scan_meta_categories": [BLISS_SCANINFO_CATEGORY],
        }

    def fill_scan_info(self, scan_info: MutableMapping) -> None:
        if not self.techniques:
            return
        scan_meta_categories = scan_info.setdefault("scan_meta_categories", list())

        if BLISS_SCANINFO_CATEGORY not in scan_meta_categories:
            scan_meta_categories.append(BLISS_SCANINFO_CATEGORY)

        nxentry_children = scan_info.get(BLISS_SCANINFO_CATEGORY)
        if nxentry_children is None:
            nxentry_children = scan_info[BLISS_SCANINFO_CATEGORY] = dict()

        self._fill_nxentry_children(nxentry_children)

    def _get_nxentry_children(self) -> Dict[str, str]:
        nxentry_children = dict()
        sorted_techniques = self._get_sorted_techniques()

        for i, technique in enumerate(sorted_techniques, 1):
            key = f"{_NEXUS_IDENTIFIER_PREFIX}{i}"
            nxentry_children[key] = technique.versioned_iri
            nxentry_children[f"{key}@type"] = "W3ID"

        return nxentry_children

    def _fill_nxentry_children(self, nxentry_children: MutableMapping) -> None:
        sorted_techniques = self._get_sorted_techniques()

        existing = {
            key: value
            for key, value in nxentry_children.items()
            if key.startswith(_NEXUS_IDENTIFIER_PREFIX) and not key.endswith("@type")
        }

        existing_iris = set(existing.values())

        used_indices = {int(key.split("_")[-1]) for key in existing}

        next_index = max(used_indices, default=0) + 1

        for technique in sorted_techniques:
            if technique.iri in existing_iris:
                continue

            key = f"{_NEXUS_IDENTIFIER_PREFIX}{next_index}"
            nxentry_children[key] = technique.versioned_iri
            nxentry_children[f"{key}@type"] = "W3ID"

            next_index += 1

    def _get_sorted_techniques(self) -> List[Technique]:
        return sorted(self.techniques, key=lambda technique: technique.primary_name)

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
        metadata = self._get_icat_metadata(techniques)
        ontology_version = self._get_ontology_version_number()
        metadata["technique_pid_esrfet_version"] = ontology_version
        for key, value in metadata.items():
            try:
                dataset[key] = value
            except KeyError:
                if key in ("technique_pid", "technique_pid_esrfet_version"):
                    _logger.warning(
                        f"Skip ICAT field '{key}' (requires pyicat-plus>=0.2)"
                    )
                    continue
                raise

    def _get_ontology_version_number(self) -> str:
        return next(iter(self.techniques)).ontology_version.lstrip("v")

    def get_dataset_metadata(self) -> Dict[str, str]:
        if not self.techniques:
            return dict()
        techniques = {
            technique.iri: technique.primary_name for technique in self.techniques
        }
        return self._get_icat_metadata(techniques)

    def _get_icat_metadata(self, techniques: Dict[str, str]) -> Dict[str, str]:
        iris, definitions = zip(*sorted(techniques.items(), key=lambda tpl: tpl[1]))
        metadata = {
            "technique_pid": " ".join(iris),
            "definition": " ".join(definitions),
        }
        if self.techniques:
            metadata["technique_pid_esrfet_version"] = (
                self._get_ontology_version_number()
            )
        return metadata
