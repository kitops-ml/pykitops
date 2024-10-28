import py
import pytest


class TestKitfileCreation:

    def test_create_full_kitfile(self, fixtures, tmpdir):
        kitfile_path = py.path.local(fixtures['Kitfile_base_thru_model'])
        kitfile = Kitfile(stream = kitfile_path)
        assert kitfile is not None