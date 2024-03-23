import pytest
from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "PaNET01196",
    }

    assert metadata.get_dataset_metadata() == dataset_metadata


def test_fill_dataset_metadata():
    metadata = get_technique_metadata("XAS")
    dataset_metadata = {
        "definition": "XAS",
        "technique_pid": "PaNET01196",
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
            "acronyms": ["XAS"],
            "names": ["x-ray absorption spectroscopy"],
            "iris": ["http://purl.org/pan-science/PaNET/PaNET01196"],
        },
    }
    assert metadata.get_scan_info() == scan_info


def test_fill_scan_info():
    metadata = get_technique_metadata("XAS")
    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS"],
            "names": ["x-ray absorption spectroscopy"],
            "iris": ["http://purl.org/pan-science/PaNET/PaNET01196"],
        },
    }

    info = {}
    metadata.fill_scan_info(info)
    assert info == scan_info

    scan_info = {
        "scan_meta_categories": ["techniques", "technique"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS"],
            "names": ["x-ray absorption spectroscopy"],
            "iris": ["http://purl.org/pan-science/PaNET/PaNET01196"],
        },
    }
    info = {
        "scan_meta_categories": ["techniques", "technique"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XRF"],
            "names": ["fluorescence microscopy"],
            "iris": ["http://purl.org/pan-science/PaNET/PaNET01113"],
        },
    }
    metadata.fill_scan_info(info)
    assert info == scan_info


def test_wrong_technique_metadata():
    with pytest.raises(KeyError, match="'WRONG' is not a known technique alias"):
        get_technique_metadata("XAS", "WRONG")


def test_empty_technique_metadata():
    metadata = get_technique_metadata()
    assert metadata.get_dataset_metadata() == dict()
    assert metadata.get_scan_info() == dict()
