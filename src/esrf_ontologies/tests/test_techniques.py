from ..technique import get_techniques
from ..technique import get_all_techniques


def test_get_all_technique():
    assert get_all_techniques()


def test_get_technique():
    all_techniques = set(get_all_techniques())
    subset = get_techniques("XRF", "XRD")
    assert subset
    assert subset < all_techniques
