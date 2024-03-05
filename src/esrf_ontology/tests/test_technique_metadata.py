import pytest
from ..metadata import get_technique_metadata


def test_single_technique_metadata():
    metadata = get_technique_metadata("XAS")

    techniques = ["XAS"]
    assert metadata.get_dataset_techniques() == techniques

    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS"],
            "names": ["x-ray absorption spectroscopy"],
            "urls": ["http://purl.org/pan-science/PaNET/PaNET01196"],
        },
    }
    assert metadata.get_scan_info() == scan_info


def test_multi_technique_metadata():
    metadata = get_technique_metadata("XRF", "XAS")

    techniques = ["XAS", "XRF"]
    assert metadata.get_dataset_techniques() == techniques

    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS", "XRF"],
            "names": ["x-ray absorption spectroscopy", "x-ray fluorescence"],
            "urls": [
                "http://purl.org/pan-science/PaNET/PaNET01196",
                "http://purl.org/pan-science/PaNET/PaNET01177",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info


def test_double_technique_metadata():
    metadata = get_technique_metadata("XRF", "XAS", "XRF", "XAS")
    assert len(metadata.techniques) == 2

    techniques = ["XAS", "XRF"]
    assert metadata.get_dataset_techniques() == techniques

    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS", "XRF"],
            "names": ["x-ray absorption spectroscopy", "x-ray fluorescence"],
            "urls": [
                "http://purl.org/pan-science/PaNET/PaNET01196",
                "http://purl.org/pan-science/PaNET/PaNET01177",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info


def test_wrong_technique_metadata():
    with pytest.raises(KeyError, match="'WRONG' is not a known technique acronym"):
        get_technique_metadata("XAS", "WRONG")


def test_empty_technique_metadata():
    metadata = get_technique_metadata()
    assert metadata.get_dataset_techniques() == list()
    assert metadata.get_scan_info() == dict()
