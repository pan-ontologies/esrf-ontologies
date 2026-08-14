import pytest

from ..technique import BLISS_SCANINFO_CATEGORY
from ..technique import get_ontology_version
from ..technique import get_ontology_version_number
from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    ontology_version = get_ontology_version_number(metadata)
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "https://w3id.org/PaN/ESRFET#XAS",
        "technique_pid_esrfet_version": ontology_version,
    }

    assert metadata.get_dataset_metadata() == dataset_metadata


def test_fill_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    ontology_version = get_ontology_version_number(metadata)
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "https://w3id.org/PaN/ESRFET#XAS",
        "technique_pid_esrfet_version": ontology_version,
    }

    dataset = {}
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = dict(dataset_metadata)
    metadata.fill_dataset_metadata(dataset_metadata)
    assert dataset == dataset_metadata


def test_get_scan_info():
    metadata = get_technique_metadata("XAS")
    ontology_version = get_ontology_version(metadata)
    scan_info = {
        "scan_meta_categories": [BLISS_SCANINFO_CATEGORY],
        BLISS_SCANINFO_CATEGORY: {
            "identifier_technique_1": f"https://w3id.org/PaN/ESRFET/{ontology_version}/#XAS",
            "identifier_technique_1@type": "W3ID",
        },
    }
    assert metadata.get_scan_info() == scan_info
    assert metadata.get_scan_metadata() == scan_info[BLISS_SCANINFO_CATEGORY]


def test_fill_scan_info():
    metadata = get_technique_metadata("XAS")
    ontology_version = get_ontology_version(metadata)
    scan_info = {
        "scan_meta_categories": [BLISS_SCANINFO_CATEGORY],
        BLISS_SCANINFO_CATEGORY: {
            "identifier_technique_1": f"https://w3id.org/PaN/ESRFET/{ontology_version}/#XAS",
            "identifier_technique_1@type": "W3ID",
        },
    }
    info = {}
    metadata.fill_scan_info(info)
    assert info == scan_info

    scan_info = {
        "scan_meta_categories": [BLISS_SCANINFO_CATEGORY, "technique"],
        BLISS_SCANINFO_CATEGORY: {
            "identifier_technique_1": f"https://w3id.org/PaN/ESRFET/{ontology_version}/#XRF",
            "identifier_technique_1@type": "W3ID",
            "identifier_technique_2": f"https://w3id.org/PaN/ESRFET/{ontology_version}/#XAS",
            "identifier_technique_2@type": "W3ID",
        },
    }
    info = {
        "scan_meta_categories": [BLISS_SCANINFO_CATEGORY, "technique"],
        BLISS_SCANINFO_CATEGORY: {
            "identifier_technique_1": f"https://w3id.org/PaN/ESRFET/{ontology_version}/#XRF",
            "identifier_technique_1@type": "W3ID",
        },
    }
    metadata.fill_scan_info(info)
    assert info == scan_info


def test_wrong_technique_metadata():
    with pytest.raises(KeyError, match="'WRONG' is not a known technique name or IRI"):
        get_technique_metadata("XAS", "WRONG")


def test_empty_technique_metadata():
    metadata = get_technique_metadata()
    assert metadata.get_dataset_metadata() == dict()
    assert metadata.get_scan_info() == dict()
    assert metadata.get_scan_metadata() is None


def test_get_metadata_from_iri():
    metadata = get_technique_metadata("https://w3id.org/PaN/ESRFET#XAS")
    dataset_metadata = metadata.get_dataset_metadata()

    assert dataset_metadata["definition"] == "XAS"
    assert dataset_metadata["technique_pid"] == "https://w3id.org/PaN/ESRFET#XAS"


def test_get_metadata_from_versioned_iri():
    version = get_ontology_version()
    metadata = get_technique_metadata(f"https://w3id.org/PaN/ESRFET/{version}/#XAS")
    dataset_metadata = metadata.get_dataset_metadata()

    assert dataset_metadata["definition"] == "XAS"
    assert dataset_metadata["technique_pid"] == "https://w3id.org/PaN/ESRFET#XAS"


def test_get_metadata_from_name():
    metadata = get_technique_metadata("xas")
    dataset_metadata = metadata.get_dataset_metadata()

    assert dataset_metadata["definition"] == "XAS"
    assert dataset_metadata["technique_pid"] == "https://w3id.org/PaN/ESRFET#XAS"
