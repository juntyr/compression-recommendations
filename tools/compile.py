import importlib.metadata
import shlex
import subprocess
from pathlib import Path

import strictyaml
from tqdm import tqdm

recommendations = Path("recommendations")

paths = sorted(recommendations.glob("*.yaml"))

commit = subprocess.run(
    shlex.split("git rev-list HEAD -1 -- recommendations tools"),
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

combined = {
    "recommendations": [1] * len(paths),
    "version": importlib.metadata.version("compression_recommendations"),
    "metadata": {
        "commit": commit,
    },
}

combined = strictyaml.as_document(
    data=combined,
    schema=strictyaml.Map(
        {
            "recommendations": strictyaml.Seq(strictyaml.Any()),
            "version": strictyaml.Str(),
            "metadata": strictyaml.MapPattern(strictyaml.Str(), strictyaml.Any()),
        }
    ),
)

for i, path in tqdm(enumerate(paths)):
    yaml = path.read_text()
    yaml2 = []
    for line in yaml.splitlines(keepends=True):
        if line.lstrip().startswith("#"):
            continue
        yaml2.append(line)
    yaml = "".join(yaml2)

    combined["recommendations"][i] = strictyaml.load(yaml)

Path("src").joinpath("compression_recommendations", "recommendations.yaml").write_text(
    """\
# Automatically compiled from recommendations/*.yaml.
# DO NOT EDIT

"""
    + combined.as_yaml()
)
