---
edit_uri: docs/recommendations.md
render_macros: true
---

# Recommendations

The following links direct to the community-created recommendation source files, which are automatically compiled into one machine-readable [`recommendations.yaml`]({{ config.repo_url }}/{{ config.edit_uri }}/src/compression_recommendations/recommendations.yaml) file.

{%- for name, path in recommendations().items() %}

- [{{ name }}]({{ config.repo_url }}/{{ config.edit_uri }}/{{ path }})

{%- endfor %}
