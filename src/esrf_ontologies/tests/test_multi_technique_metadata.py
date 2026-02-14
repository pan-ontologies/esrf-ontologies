from ..technique import get_technique_metadata


def test_get_dataset_metadata():
    metadata = get_technique_metadata("XRF", "XAS")
    dataset_metadata = {
        "definition": "XAS XRF",
        "technique_pid": " ".join(
            [
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
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
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
            ]
        ),
    }

    dataset = dict(dataset_metadata)
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRF",
        "technique_pid": "https://w3id.org/PaN/ESRFET#XRF",
    }
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {}
    metadata.fill_dataset_metadata(dataset)
    assert dataset == dataset_metadata

    dataset = {
        "definition": "XRD",
        "technique_pid": "https://w3id.org/PaN/ESRFET#XRD",
    }
    dataset_metadata = {
        "definition": "XAS XRD XRF",
        "technique_pid": " ".join(
            [
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRD",
                "https://w3id.org/PaN/ESRFET#XRF",
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
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
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
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
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
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
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
                "https://w3id.org/PaN/ESRFET#XAS",
                "https://w3id.org/PaN/ESRFET#XRF",
            ],
        },
    }
    assert metadata.get_scan_info() == scan_info
    assert metadata.get_scan_metadata() == scan_info["techniques"]
