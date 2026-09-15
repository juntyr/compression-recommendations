# Recommendations for Safe Lossy Compression of weather and climate data

[![image](https://img.shields.io/github/actions/workflow/status/juntyr/compression-recommendations/ci.yml?branch=main)](https://github.com/juntyr/compression-recommendations/actions/workflows/ci.yml?query=branch%3Amain)
[![image](https://img.shields.io/pypi/v/compression-recommendations.svg)](https://pypi.python.org/pypi/compression-recommendations)
[![image](https://img.shields.io/pypi/l/compression-recommendations.svg)](https://github.com/juntyr/compression-recommendations/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/compression-recommendations.svg)](https://pypi.python.org/pypi/compression-recommendations)
[![image](https://readthedocs.org/projects/compression-recommendations/badge/?version=latest)](https://compression-recommendations.readthedocs.io/en/latest/?badge=latest)
[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.22761209.svg)](https://doi.org/10.5281/zenodo.22761209)


What lossy compression is safe when using lossy compression on weather and climate data?

This repository contains community-provided [recommendations](recommendations) that are automatically compiled into one machine-readable [`recommendations.yaml`](src/compression_recommendations/recommendations.yaml) file.
These recommendations can then be used by external tools to automatically recommend appropriate safety requirements for compressing various weather and climate data.

This repository also provides the `compression-recommendations` Python package for loading these recommendations and inspecting them in the strongly typed `Recommendations` data structure.

Furthermore, we provide the following integrations:

- `compression-requirement-checks` checks whether safety requirements are upheld by a lossy-decompressed reconstruction of the original data.
- `compression-requirement-safeguards` translates safety requirements into [compression safeguards](https://compression-safeguards.readthedocs.io) that can be wrapped around any compressor to guarantee that the requirements are fulfilled.


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

Please refer to the [CITATION.cff](CITATION.cff) file and refer to <https://citation-file-format.github.io> to extract the citation in a format of your choice.


## License

Licensed under the Mozilla Public License, Version 2.0 ([LICENSE](LICENSE) or https://www.mozilla.org/en-US/MPL/2.0/).


## Funding

The outline for the recommendations have been developed as part of [ESiWACE3](https://www.esiwace.eu), the third phase of the Centre of Excellence in Simulation of Weather and Climate in Europe.

Funded by the European Union. This work has received funding from the European High Performance Computing Joint Undertaking (JU) under grant agreement No 101093054.
