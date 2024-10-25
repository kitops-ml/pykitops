from _pytest.compat import LEGACY_PATH
import py
import pytest
from pathlib import Path
from modelkit.modelkit_types import YAML
from modelkit.modelpart import ModelPart


class TestModelPart:

    testdata = [
        (Path("config.json"), "config", "config file", "type: config file"),
        (Path("config.json"), "config", None, "name: config"),
        (Path("config.json"), None, None, "path: config.json"),
        ("config.json", None, None, "path: config.json")
    ]
    @pytest.mark.parametrize("path,name,type,expected", testdata)
    def test_modelpart_init(self, path: str|Path, name: str|None, type: str|None, expected: YAML):
        modelpart: ModelPart = ModelPart(path = path, name = name, type = type)
        print(modelpart.create_yaml())

        assert expected in modelpart.create_yaml()
        
    #def test_modelpart_init(self, fixtures: dict[str, str], tmpdir: LEGACY_PATH):
    #    base_file_path = py.path.local(fixtures['modelparts.yaml'])
    #    modelpart = ModelPart(path)