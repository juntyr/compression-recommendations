import importlib.metadata
import shlex
import subprocess
from pathlib import Path

from semver import Version
from tqdm import tqdm

from compression_recommendations import Recommendations
from compression_recommendations.recommendation import Recommendation

commit = subprocess.run(
    shlex.split(
        f"git rev-list HEAD -1 -- {Path('recommendations', '*.yaml')} {Path(__file__)}"
    ),
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

recommendations = []
for path in tqdm(sorted(Path("recommendations").glob("*.yaml"))):
    with path.open("r") as f:
        recommendations.append(Recommendation.load(f))

recommendations = Recommendations(
    recommendations=recommendations,
    version=Version.parse(importlib.metadata.version("compression_recommendations")),
    metadata={"commit": commit},
)

with (
    Path("src")
    .joinpath("compression_recommendations", "recommendations.yaml")
    .open("w") as f
):
    f.write("""\
# Automatically compiled from recommendations/*.yaml.
# DO NOT EDIT

""")
    recommendations.dump(f)
