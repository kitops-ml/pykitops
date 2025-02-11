from pathlib import Path

from kitops.modelkit.kitfile import Kitfile


class TestKitfileCreation:
    def test_create_full_kitfile(self, fixtures: dict[str, Path]):
        kitfile_path = fixtures["Kitfile_full"]
        kitfile = Kitfile(path=str(kitfile_path))
        assert kitfile is not None
