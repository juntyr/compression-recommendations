---
edit_uri: docs/index.md
render_macros: true
---

# Recommendations for Safe Lossy Compression of weather and climate data

What lossy compression is safe when using lossy compression on weather and climate data?

This repository contains community-provided [recommendations](recommendations.md) that are automatically compiled into one machine-readable [`recommendations.yaml`]({{ config.repo_url }}/{{ config.edit_uri }}/src/compression_recommendations/recommendations.yaml) file.
These recommendations can then be used by external tools to automatically recommend appropriate safety requirements for compressing various weather and climate data.

This repository also provides the [`compression-recommendations`][compression_recommendations] Python package for loading these recommendations and inspecting them in the strongly typed [`Recommendations`][compression_recommendations.Recommendations] data structure.

Furthermore, we provide the following integrations:

- [`compression-requirement-checks`][compression_requirement_checks] checks whether safety requirements are upheld by a lossy-decompressed reconstruction of the original data.
- [`compression-requirement-safeguards`][compression_requirement_safeguards] translates safety requirements into [compression safeguards](https://compression-safeguards.readthedocs.io) that can be wrapped around any compressor to guarantee that the requirements are fulfilled.


## Contributing: What should be recommended?

That is up to *you*, the community, to decide!

- You can *add comments* to any recommendation to elaborate or discuss different requirements.
- You can *propose edits* to any recommendation, which we accept once a new consensus has been reached.
- You can *create new recommendations* for new variables or to specialise existing requirements for specific cases.
- You can *merge multiple recommendations* to generalise them.
- You can *propose new filters* to select which recommendations should apply, or *new kinds of requirements*.


## Glossary

**Compression**
: Reducing the number of bits needed to store some data.

**Lossy Compression**
: Compression that may only produce an approximation of the original data during decompression.

**Filter**
: Criteria, or a composition of multiple criteria, that select which requirements should apply.

**Safety Requirement**
: A property, e.g. an error bound, or a composition of multiple properties, that the lossy-compressed data must fulfil with respect to the original uncompressed data.


## Citation
Please refer to the [CITATION.cff]({{ config.repo_url }}/{{ config.edit_uri }}/CITATION.cff) file and refer to <https://citation-file-format.github.io> to extract the citation in a format of your choice.


## Funding

The outline for the recommendations have been developed as part of [ESiWACE3](https://www.esiwace.eu), the third phase of the Centre of Excellence in Simulation of Weather and Climate in Europe.

Funded by the European Union. This work has received funding from the European High Performance Computing Joint Undertaking (JU) under grant agreement No 101093054.
