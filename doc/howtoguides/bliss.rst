Publish technique metadata in Bliss
===================================

Use the scan metadata mechanism in `BLISS <https://bliss.gitlab-pages.esrf.fr/bliss/>`_ to add
metadata automatically to any scan and dataset based on the content of the scan. For example any scan
that has an "energy" counter is an "XAS" scan:

.. code:: python

    from bliss import current_session
    from esrf_ontologies import technique

    def add_xas_technique(scan):
        channels = scan.scan_info.get("channels", dict())
        if "energy" in channels:
            metadata_generator = technique.get_technique_metadata("XAS")
            metadata.fill_dataset_metadata(current_session.scan_saving.dataset)
            return metadata_generator.get_scan_metadata()

    scan_meta.add_categories({"techniques"})
    scan_meta.techniques.timing = META_TIMING.START
    scan_meta.techniques.set("add_xas_technique", add_xas_technique)

Note that `get_technique_metadata` accepts one or more technique names or acronyms.

When the beamline has technique specific commands instead of the generic BLISS scan command
it can be done like this

.. code:: python

    from bliss import setup_global
    from bliss import current_session
    from esrf_ontologies import technique

    def xas_scan(start, stop, intervals, count_time, scan_info=None):
        metadata_generator = technique.get_technique_metadata("XAS")

        metadata.fill_dataset_metadata(current_session.scan_saving.dataset)

        if scan_info is None:
            scan_info=metadata_generator.get_scan_info()
        else:
            metadata_generator.fill_scan_info(scan_info)

        setup_global.ascan(setup_global.energy, start, stop, intervals, count_time, scan_info=scan_info)

Adding the same technique to a dataset several times is not a problem; a unique list of techniques
is maintained, preventing duplicates.