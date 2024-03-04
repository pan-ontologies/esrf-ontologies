ESRF Ontology |version|
=======================

.. code::python

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
