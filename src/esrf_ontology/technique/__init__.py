from .types import Technique, TechniqueMetadata
from .panet import get_techniques


def get_technique_metadata(*aliases) -> TechniqueMetadata:
    return TechniqueMetadata(
        techniques={get_technique(alias) for alias in sorted(set(aliases))}
    )


def get_technique(alias: str) -> Technique:
    try:
        return get_techniques()[alias]
    except KeyError:
        raise KeyError(f"'{alias}' is not a known technique alias") from None
