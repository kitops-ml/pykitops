from pathlib import Path

from kitops.modelkit.kitfile import Kitfile


class TestKitfileCreation:
    def test_create_full_kitfile(self, fixtures: dict[str, Path]):
        kitfile_path = fixtures["Kitfile_full"]
        kitfile = Kitfile(path=str(kitfile_path))
        assert kitfile is not None
        assert kitfile.manifestVersion == "1.0"
        assert kitfile is not None and kitfile.package.name == "Titanic-Survivability-Predictor"
        assert kitfile is not None and kitfile.model.name == "titanic-survivability-predictor"
    
    def test_create_blank_kitfile(self):
        kitfile = Kitfile()
        assert kitfile is not None and kitfile == Kitfile()

    def test_create_from_template(self, fixtures: dict[str, Path]):
        kitfile_path = fixtures["Kitfile_full"]
        kitfile = Kitfile(path=str(kitfile_path), manifestVersion="6.9.0")
        assert kitfile is not None and kitfile.manifestVersion == "6.9.0"