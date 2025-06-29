# ESRF Ontologies

The *ESRF Ontologies* project provides ontologies related to [ESRF](https://esrf.fr/) data acquisition.

Ontologies:

* *ESRFET* is an ontology of experimental techniques used at the ESRF connected to
  the [PaNET](https://doi.org/10.5281/zenodo.4806026) ontology.

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
