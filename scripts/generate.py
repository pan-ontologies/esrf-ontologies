import os
import sys
from typing import Sequence, Generator, List

from tabulate import tabulate

from esrf_ontology.technique.types import Technique
from esrf_ontology.technique import get_all_techniques


def main():
    docdir = os.path.join(os.path.dirname(__file__), "..", "doc")

    headers = ["Alias", "Acronym", "Name", "PID"]
    table = [
        row
        for alias, techniques in sorted(get_all_techniques().items())
        for row in _iter_rows(alias, techniques)
    ]

    with open(os.path.join(docdir, "techniques.rst"), "w") as f:
        f.write(".. _techniques:\n\n")
        f.write("Techniques\n==========\n\n")
        f.write(
            "The **alias** is used in :meth:`esrf_ontology.technique.get_technique_metadata`.\n\n"
        )
        f.write(tabulate(table, headers, tablefmt="rst"))


def _iter_rows(
    alias, techniques: Sequence[Technique]
) -> Generator[List[str], None, None]:
    for technique in sorted(techniques, key=lambda tech: tech.acronym):
        yield [
            alias,
            technique.acronym,
            technique.name,
            f"`{technique.pid} <{technique.iri}>`_",
        ]
        alias = ""


if __name__ == "__main__":
    sys.exit(main())
