from dataclasses import dataclass

_PANET_ID_TEMPLATE = "http://purl.org/pan-science/PaNET/PaNET{:05d}"


@dataclass(frozen=True)
class Technique:
    acronym: str
    name: str
    panetid: int

    @property
    def url(self) -> str:
        return _PANET_ID_TEMPLATE.format(self.panetid)


def get_technique(alias: str) -> Technique:
    try:
        return _TECHNIQUES[alias]
    except KeyError:
        raise KeyError(f"'{alias}' is not a known technique acronym") from None


_TECHNIQUES = {
    "XAS": Technique(acronym="XAS", name="x-ray absorption spectroscopy", panetid=1196),
    "XRF": Technique(acronym="XRF", name="x-ray fluorescence", panetid=1177),
}
