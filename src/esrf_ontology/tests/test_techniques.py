from ..technique import get_techniques
from ..technique import get_all_techniques


def test_get_all_technique():
    assert get_all_techniques()


def test_get_technique():
    all_techniques = {
        tech for techniques in get_all_techniques().values() for tech in techniques
    }
    subset = get_techniques("XRF", "XRD")
    assert subset
    assert subset < all_techniques
