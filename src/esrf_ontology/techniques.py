from dataclasses import dataclass

from . import panet_techniques


_PANET_ID_TEMPLATE = "http://purl.org/pan-science/PaNET/PaNET{:05d}"


@dataclass(frozen=True)
class Technique:
    acronym: str
    name: str
    panetid: int

    @property
    def url(self) -> str:
        return _PANET_ID_TEMPLATE.format(self.panetid)

    class Config:
        frozen = True


def get_technique(alias: str) -> Technique:
    try:
        return panet_techniques.get_techniques_panet()[alias]
    except KeyError:
        raise KeyError(f"'{alias}' is not a known technique alias") from None
