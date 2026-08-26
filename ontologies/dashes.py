"""Normalization of non-ASCII dash-like characters to the ASCII hyphen-minus."""

NON_ASCII_DASHES = {
    "‐": "Hyphen",
    "‑": "Non-breaking hyphen",
    "‒": "Figure dash",
    "–": "En dash",
    "—": "Em dash",
    "―": "Horizontal bar",
    "−": "Minus sign",
    "﹘": "Small em dash",
    "－": "Fullwidth hyphen-minus",
    "᠆": "Mongolian todo soft hyphen",
}

DASH_TRANSLATION = str.maketrans({char: "-" for char in NON_ASCII_DASHES})


def normalize_dashes(text: str) -> str:
    return text.translate(DASH_TRANSLATION)
