from pathlib import Path

from .plotter import Plotter


if __name__ == "__main__":
    for profile in Path("assets/profiles/").glob("*.toml"):
        Plotter(profile)

