ESRF Ontology |version|
=======================

The ESRF ontology provides a python API to all ontologies used on ESRF data acquisition.

* Metadata for techniques within the photon and neutron (PaN) domain from the `PaNET Ontology <https://doi.org/10.5281/zenodo.4806026>`_.

Technique in Bliss
------------------

Get the :ref:`technique metadata <techniques>` for one of more aliases

.. code:: python

    from esrf_ontology.technique import get_technique_metadata

    metadata = get_technique_metadata("XAS", "XRF")

Add technique metadata to the BLISS dataset metadata for the ESRF data portal

.. code:: python

    from bliss import current_session

    metadata.fill_dataset_metadata(current_session.scan_saving.dataset)

Add technique metadata to the BLISS scan info to be saved in HDF5 by the NeXus writer

.. code:: python

    ascan(energy, 9.01, 9.3, 600, 0.1, scan_info=metadata.get_scan_info())

Or when it needs to be merged it with already existing BLISS scan info

.. code:: python

    metadata.fill_scan_info(scan_info)
    ascan(energy, 9.01, 9.3, 600, 0.1, scan_info=scan_info)

.. toctree::
    :hidden:
    
    techniques
    api
