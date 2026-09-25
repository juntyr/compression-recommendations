---
edit_uri: docs/try-repl.md
render_macros: true
---

# Explore the `compression-recommendations` using JupyterLite

/// details | **Warning:** JupyterLite may not work in every web browser
    type: warning
<img src="https://baseline.js.org/features/wasm-multi-memory/responsive-adaptive.svg" alt="Baseline Status: Multi-memory (WebAssembly)" style="width: 100%; height: auto;" />
///

<iframe id="try-repl-jupyterlite" width="100%" height="550px" referrerpolicy="no-referrer"></iframe>

<script>
  window.addEventListener("load", () => {
    document.getElementById("try-repl-jupyterlite").src = "https://lab.climet.eu/v0.5.0/repl/index.html?kernel=python&toolbar=1&code=" + encodeURIComponent(`\
# install the compression-recommendations
%pip install compression-recommendations=={{ version('compression_recommendations') }}\
`) + "&code=" + encodeURIComponent(`\
from compression_recommendations import Recommendations\
`) + "&code=" + encodeURIComponent(`\
# load the community-provided recommendations
recommendations = Recommendations.provide\
`) + "&code=" + encodeURIComponent(`\
# search the recommendations
recommendations.search(
    markers={ "cf-short-name": "cc", "level-kind": "pressure" }
)\
`) + "&pyodideKernelPackages=" + encodeURIComponent(JSON.stringify({
  "$concat": [
    // example packages
    "semver",
    "strictyaml",
    "typed-classproperties",
    "typing-extensions",
  ]
}));
  });
</script>
