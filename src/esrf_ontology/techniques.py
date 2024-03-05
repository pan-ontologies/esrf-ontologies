from dataclasses import dataclass
from pydantic import BaseModel

from . import panet_techniques


_PANET_ID_TEMPLATE = "http://purl.org/pan-science/PaNET/PaNET{:05d}"


class TechniqueModel(BaseModel):
    acronym: str
    name: str
    panetid: int

    @property
    def url(self) -> str:
        return _PANET_ID_TEMPLATE.format(self.panetid)
    
    class Config:
        frozen = True


def get_technique(alias: str) -> TechniqueModel:
    try:
        return _ALIAS_TO_TECHNIQUE[alias]
    except KeyError:
        raise KeyError(f"'{alias}' is not a known technique alias") from None



_ALIAS_TO_TECHNIQUE = panet_techniques.get_techniques_panet()