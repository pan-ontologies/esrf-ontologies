Ontological Definition of Experimental Techniques
=================================================

In the :ref:`ESRFET <techniques>` ontology, each experimental technique is defined by describing
the essential features that characterize it — such as what it measures, what kind of input it requires,
and how the measurement is performed.

These definitions are encoded using formal logic (OWL), but at a high level, each technique is described as:

- A type of experimental technique
- A combination of specific conditions that must be met

These conditions typically include:

- What kind of physical interaction the technique is based on (e.g., diffraction, fluorescence)
- What properties are being measured (e.g., energy, intensity)
- What kind of input is required (e.g., x-rays, electrons)
- What kind of detector or measurement method is used (e.g., energy-dispersive detector)

By using this formal structure, the ontology allows researchers and machines to:

- Search for techniques based on specific properties
- Automatically classify or compare techniques
- Check whether a technique meets a set of criteria

New techniques can be added simply by describing their key characteristics using the same structure.
