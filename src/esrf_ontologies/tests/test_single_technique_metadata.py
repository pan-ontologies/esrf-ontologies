import pytest
from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "http://purl.org/pan-science/ESRFET#XAS",
    }

    assert metadata.get_dataset_metadata() == dataset_metadata


def test_fill_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "http://purl.org/pan-science/ESRFET#XAS",
    }

    dataset = {}
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = dict(dataset_metadata)
    metadata.fill_dataset_metadata(dataset_metadata)
    assert dataset == dataset_metadata


def test_get_scan_info():
    metadata = get_technique_metadata("XAS")
    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XAS"],
            "iris": ["http://purl.org/pan-science/ESRFET#XAS"],
        },
    }
    assert metadata.get_scan_info() == scan_info
    assert metadata.get_scan_metadata() == scan_info["techniques"]


def test_fill_scan_info():
    metadata = get_technique_metadata("XAS")
    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XAS"],
            "iris": ["http://purl.org/pan-science/ESRFET#XAS"],
        },
    }

    info = {}
    metadata.fill_scan_info(info)
    assert info == scan_info

    scan_info = {
        "scan_meta_categories": ["techniques", "technique"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XAS", "XRF"],
            "iris": [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ],
        },
    }
    info = {
        "scan_meta_categories": ["techniques", "technique"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XRF"],
            "iris": ["http://purl.org/pan-science/ESRFET#XRF"],
        },
    }
    metadata.fill_scan_info(info)
    assert info == scan_info


def test_wrong_technique_metadata():
    with pytest.raises(KeyError, match="'WRONG' is not a known technique name"):
        get_technique_metadata("XAS", "WRONG")


def test_empty_technique_metadata():
    metadata = get_technique_metadata()
    assert metadata.get_dataset_metadata() == dict()
    assert metadata.get_scan_info() == dict()
    assert metadata.get_scan_metadata() is None
