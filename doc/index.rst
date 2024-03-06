ESRF Ontology |version|
=======================

The ESRF ontology currently only provides a python API to the `PaNET Ontology <https://doi.org/10.5281/zenodo.4806026>`_
for techniques within the photon and neutron (PaN) domain.

Technique in Bliss
------------------

Define technique related metadata for HDF5 and the data portal in Bliss:

.. code:: python

    from bliss import current_session
    from esrf_ontology.metadata import get_technique_metadata

    metadata = get_technique_metadata("XAS")

    # Data Portal metadata
    current_session.scan_saving.dataset.add_techniques(*metadata.get_dataset_techniques())

    # HDF5 file metadata
    ascan(energy, 9.01, 9.3, 600, 0.1, scan_info=metadata.get_scan_info())

.. toctree::
    :hidden:
    
    api
