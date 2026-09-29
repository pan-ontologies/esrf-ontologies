# ESRF Ontologies

The *ESRF Ontologies* project provides ontologies related to [ESRF](https://esrf.fr/) data acquisition.

Ontologies maintained by the ESRF in this repository:

* *ESRFET* is an ontology of experimental techniques used at the ESRF connected to
  the [PaNET](https://doi.org/10.5281/zenodo.4806026) ontology.
* *ESRFFAIR* is an ontology of experiment participation (work in progress).

Ontologies maintained elsewhere and included here as copies of their upstream source:

| Ontology | Maintained by | Upstream source |
|----------|---------------|-----------------|
| *PaNET* | [PaN Ontologies](https://github.com/pan-ontologies) (originally ExPaNDS) | https://github.com/pan-ontologies/PaNET |
| *NeXus Ontology* | [NIAC](https://www.nexusformat.org/NIAC.html), developed by [FAIRmat](https://www.fairmat-nfdi.eu/) | https://github.com/nexusformat/NeXusOntology |

Python API:

* Generate technique metadata for ESRF data producers to save in [NeXus-compliant](https://www.nexusformat.org/)
  HDF5 and the [ESRF data portal](https://data.esrf.fr).

## Getting started

Install from pypi

```bash
pip install esrf-ontologies
```

Retrieve technique metadata for one or more techniques

```python
from esrf_ontologies import technique

technique_metadata = technique.get_technique_metadata("XAS", "XRF")
dataset_metadata = technique_metadata.get_dataset_metadata()
scan_metadata = technique_metadata.get_scan_metadata()
```

## Documentation

https://esrf-ontologies.readthedocs.io
