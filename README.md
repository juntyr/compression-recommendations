# Recommendations for Safe Lossy Compression of weather and climate data

What lossy compression is safe when using lossy compression on weather and climate data?

This repository contains community-created [recommendations](recommendations) that are automatically compiled into one machine-readable [`recommendations.yaml`](recommendations.yaml) file.
These recommendations can then be used by external tools to automatically recommend appropriate safety requirements for compressing various weather and climate data.

## Contributing: What should be recommended?

That is up to *you* to decide!
- You can add comments to any recommendation to elaborate or discuss different requirements.
- You can propose edits to any recommendation, which we accept once a new consensus has been reached.
- You can create new recommendations for new variables or to specialise existing requirements for specific cases.
- You can merge multiple recommendations to generalise them.
- You can propose new filters to select which recommendations should apply, or new kinds of requirements.


## Glossary

Compression
: Reducing the number of bits needed to store some data.

Lossy Compression
: Compression that may only produce an approximation of the original data during decompression.

Filter
: Criteria, or a composition of multiple criteria, that select which requirements should apply.

Safety Requirement
: A property, e.g. an error bound, that the lossy-compressed data must fulfil with respect to the original uncompressed data.

Pointwise Absolute Error Bound
: $|\hat{x} - x| <= \epsilon_{abs}$ for the original data $x$ and decompressed data $\hat{x}$

Pointwise Relative Error Bound
: $|\hat{x} - x| <= (|x| \cdot \epsilon_{rel})$ for the original data $x$ and decompressed data $\hat{x}$


## Citation

Please refer to the [CITATION.cff](CITATION.cff) file and refer to <https://citation-file-format.github.io> to extract the citation in a format of your choice.


## License

Licensed under the Mozilla Public License, Version 2.0 ([LICENSE](LICENSE) or https://www.mozilla.org/en-US/MPL/2.0/).


## Funding

The outline for the recommendations have been developed as part of [ESiWACE3](https://www.esiwace.eu), the third phase of the Centre of Excellence in Simulation of Weather and Climate in Europe.

Funded by the European Union. This work has received funding from the European High Performance Computing Joint Undertaking (JU) under grant agreement No 101093054.
