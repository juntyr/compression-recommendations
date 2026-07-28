from pathlib import Path

import gitinfo
import strictyaml
from tqdm import tqdm

recommendations = Path("recommendations")

paths = sorted(recommendations.glob("*.yaml"))

combined = {
    "recommendations": [1] * len(paths),
    "version": "0.1.0",
    "metadata": {
        "commit": gitinfo.get_git_info()["commit"],
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
