import importlib.metadata
from pathlib import Path

from compression_recommendations import Recommendations


def define_env(env):
    @env.macro
    def recommendations():
        return Recommendations.provide

    @env.macro
    def recommendation_files():
        return {
            path.name: str(path)
            for path in sorted(Path("recommendations").glob("*.yaml"))
        }

    @env.macro
    def version(x):
        return importlib.metadata.version(x)
