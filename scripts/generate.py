import os
import sys
from tabulate import tabulate
from esrf_ontology.technique import get_techniques


def main():
    docdir = os.path.join(os.path.dirname(__file__), "..", "doc")

    headers = ["PID", "Alias", "Acronym", "Name"]
    table = [
        [
            f"`{technique.pid} <{technique.iri}>`_",
            alias,
            technique.acronym,
            technique.name,
        ]
        for alias, technique in sorted(
            get_techniques().items(), key=lambda tpl: tpl[1].acronym
        )
    ]

    with open(os.path.join(docdir, "techniques.rst"), "w") as f:
        f.write(".. _techniques:\n\n")
        f.write("Techniques\n==========\n\n")
        f.write(
            "The **alias** is used in :meth:`esrf_ontology.technique.get_technique_metadata`.\n\n"
        )
        f.write(tabulate(table, headers, tablefmt="rst"))


if __name__ == "__main__":
    sys.exit(main())
