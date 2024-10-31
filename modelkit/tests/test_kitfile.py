from _pytest.compat import LEGACY_PATH
import py
import pytest
from modelkit.kitfile import Kitfile

class TestKitfileCreation:

    def test_create_full_kitfile(self, fixtures: dict[str, str], tmpdir: LEGACY_PATH):
        kitfile_path = py.path.local(fixtures['Kitfile_full'])
        kitfile = Kitfile(path = kitfile_path)
        assert kitfile is not None