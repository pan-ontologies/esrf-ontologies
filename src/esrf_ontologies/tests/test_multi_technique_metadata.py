from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XRF", "XAS")
    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": " ".join(
            [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ]
        ),
    }

    assert metadata.get_dataset_metadata() == dataset_metadata


def test_fill_dataset_metadata():
    metadata = get_technique_metadata("XRF", "XAS")
    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": " ".join(
            [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ]
        ),
    }

    dataset = dict(dataset_metadata)
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRF",
        "technique_pid": "http://purl.org/pan-science/ESRFET#XRF",
    }
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {}
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRD",
        "technique_pid": "http://purl.org/pan-science/ESRFET#XRD",
    }
    dataset_metadata = {
        "definition": "XAS XRD XRF",
        "technique_pid": " ".join(
            [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRD",
                "http://purl.org/pan-science/ESRFET#XRF",
            ]
        ),
    }
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata


def test_get_scan_info():
    metadata = get_technique_metadata("XRF", "XAS")
    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XAS", "XRF"],
            "iris": [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info
    assert metadata.get_scan_metadata() == scan_info["techniques"]


def test_fill_scan_info():
    metadata = get_technique_metadata("XRF", "XAS")
    scan_info = {
        "scan_meta_categories": ["technique", "techniques"],
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
        "technique_pid": " ".join(
            [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ]
        ),
    }
    assert metadata.get_dataset_metadata() == dataset_metadata

    scan_info = {
        "scan_meta_categories": ["techniques"],
        "techniques": {
            "@NX_class": "NXnote",
            "names": ["XAS", "XRF"],
            "iris": [
                "http://purl.org/pan-science/ESRFET#XAS",
                "http://purl.org/pan-science/ESRFET#XRF",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info
    assert metadata.get_scan_metadata() == scan_info["techniques"]
