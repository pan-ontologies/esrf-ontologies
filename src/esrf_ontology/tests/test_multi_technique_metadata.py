from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XRF", "XAS")
    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": "PaNET01196 PaNET01113",
    }

    assert metadata.get_dataset_metadata() == dataset_metadata


def test_fill_dataset_metadata():
    metadata = get_technique_metadata("XRF", "XAS")
    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": "PaNET01196 PaNET01113",
    }

    dataset = dict(dataset_metadata)
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRF",
        "technique_pid": "PaNET01113",
    }
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {}
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRD",
        "technique_pid": "PaNET01216",
    }
    dataset_metadata = {
        "definition": "XAS XRD XRF",
        "technique_pid": "PaNET01196 PaNET01216 PaNET01113",
    }
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata


def test_get_scan_info():
    metadata = get_technique_metadata("XRF", "XAS")
    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS", "XRF"],
            "names": ["x-ray absorption spectroscopy", "fluorescence microscopy"],
            "iris": [
                "http://purl.org/pan-science/PaNET/PaNET01196",
                "http://purl.org/pan-science/PaNET/PaNET01113",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info


def test_fill_scan_info():
    metadata = get_technique_metadata("XRF", "XAS")
    scan_info = {
        "scan_meta_categories": ["technique", "techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS", "XRF"],
            "names": ["x-ray absorption spectroscopy", "fluorescence microscopy"],
            "iris": [
                "http://purl.org/pan-science/PaNET/PaNET01196",
                "http://purl.org/pan-science/PaNET/PaNET01113",
            ],
        },
    }

    info = {
        "scan_meta_categories": ["technique"],
        "techniques": None,
    }
    metadata.fill_scan_info(info)
    assert info == scan_info


def test_double_technique_metadata():
    metadata = get_technique_metadata("XRF", "XAS", "XRF", "XAS")
    assert len(metadata.techniques) == 2

    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": "PaNET01196 PaNET01113",
    }
    assert metadata.get_dataset_metadata() == dataset_metadata

    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "acronyms": ["XAS", "XRF"],
            "names": ["x-ray absorption spectroscopy", "fluorescence microscopy"],
            "iris": [
                "http://purl.org/pan-science/PaNET/PaNET01196",
                "http://purl.org/pan-science/PaNET/PaNET01113",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info
