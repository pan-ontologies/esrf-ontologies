ESRF Ontologies |version|
=========================

The *ESRF Ontologies* project provides ontologies related to `ESRF <https://esrf.fr/>`_ data acquisition.

Ontologies:

* *ESRFET* is an ontology of experimental techniques used at the ESRF connected to
  the `PaNET <https://doi.org/10.5281/zenodo.4806026>`_ ontology.

Python API's:

* Generate technique metadata for ESRF data producers to save in `NeXus-compliant <https://www.nexusformat.org/>`_
  HDF5 and the `ESRF data portal <https://data.esrf.fr>`_.

Python API
----------

Get the :ref:`technique metadata <techniques>` for one of more techniques

.. code:: python

    from esrf_ontologies import technique

    technique_metadata = technique.get_technique_metadata("XAS", "XRF")
    dataset_metadata = technique_metadata.get_dataset_metadata()
    scan_metadata = technique_metadata.get_scan_metadata()

Get all techniques or a subset based on technique name or acronym

.. code:: python

    all_techniques = technique.get_all_techniques()
    techniques = technique.get_techniques("XAS", "XRF")

.. toctree::
    :hidden:

    howtoguides
    explanations
    esrfet
    api
