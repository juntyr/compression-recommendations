from pathlib import Path


def define_env(env):
    @env.macro
    def recommendations():
        return {
            path.name: str(path)
            for path in sorted(Path("recommendations").glob("*.yaml"))
        }
