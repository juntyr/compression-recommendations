import importlib.metadata
import shlex
import subprocess
from pathlib import Path

from packaging.version import Version as PyPIVersion
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

package_version = importlib.metadata.version("compression_recommendations")

# based on https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html#from-pypi-to-semver
pyversion = PyPIVersion(package_version)
pre = None if not pyversion.pre else "".join([str(i) for i in pyversion.pre])
version = Version(*pyversion.release, prerelease=pre, build=pyversion.dev)

recommendations = Recommendations(
    recommendations=recommendations,
    version=version,
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
