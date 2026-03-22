import re

from ..technique import get_all_techniques
from ..technique import get_ontology_version
from ..technique import get_ontology_version_number
from ..technique import get_technique
from ..technique import get_techniques


def test_get_all_technique():
    assert get_all_techniques()


def test_get_techniques():
    all_techniques = set(get_all_techniques())
    subset = get_techniques("XRF", "XRD")
    assert subset
    assert subset < all_techniques


def test_get_technique():
    all_techniques = set(get_all_techniques())
    technique = get_technique("XRF")
    assert technique in all_techniques


def test_get_technique_by_iri():
    all_techniques = set(get_all_techniques())
    technique = get_technique("https://w3id.org/PaN/ESRFET#XRF")
    assert technique in all_techniques


def test_ontology_version():
    version = get_ontology_version()
    pattern = r"^v\d+\.\d+\.\d+$"
    assert re.match(pattern, version)


def test_ontology_version_number():
    version_number = get_ontology_version_number()
    pattern = r"^\d+\.\d+\.\d+$"
    assert re.match(pattern, version_number)
