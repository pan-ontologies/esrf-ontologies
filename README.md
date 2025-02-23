# ESRF Ontology

The ESRF ontology provides a python API to all ontologies used on ESRF data acquisition.

* Metadata for techniques within the photon and neutron (PaN) domain from the [PaNET Ontology](https://doi.org/10.5281/zenodo.4806026).

## Getting started

Install from pypi

```bash
pip install esrf-ontologies
```

Retrieve technique metadata for one or more technique aliases

```python
from esrf_ontologies.technique import get_technique_metadata

metadata = get_technique_metadata("XAS", "XRF")
```

## Documentation

https://esrf-ontologies.readthedocs.io
