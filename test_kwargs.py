import yaml
from pathlib import Path
from typing import Any, Dict, List, Set

class Kitfile:
    def __init__(self, path = None):
        self._data = {}
        self._kitfile_allowed_keys = {'manifestVersion', 'package', 
                                     'code', 'datasets', 'docs', 'model'}
        # initialize an empty kitfile object
        self.manifestVersion = ""
        self.package = {"name": "", "version": "", "description": "", 
                        "authors": []}
        self.code = []
        self.datasets = []
        self.docs = []
        self.model = {"name": "", "path": "", "description": "", 
                      "framework": "", "license": "", "version": "", 
                      "parts": [], "parameters": ""}

        if path:
            self.load_from_file(path)

    def load_from_file(self, path):
        kitfile_path = Path(path)
        if not kitfile_path.exists():
            raise ValueError(f"Path '{kitfile_path}' does not exist.")
        
        # try to load the kitfile
        try:
            with open(kitfile_path, 'r') as kitfile:
            # Load the yaml data
                data = yaml.safe_load(kitfile)
        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                raise yaml.YAMLError(
                            "Error parsing Kitfile at " +
                            f"line{mark.line+1}, " +
                            f"column:{mark.column+1}.") from e
            else:
                raise

        try:
            self.validate_dict(value=data, 
                               allowed_keys=self._kitfile_allowed_keys)
        except ValueError as e:
            raise ValueError(
                    "Kitfile must be a dictionary with allowed " +
                     f"keys: {', '.join(self._kitfile_allowed_keys)}"
                    ) from e
        # kitfile has been successfully loaded into data
        self.validate_and_set_attributes(data)

    def validate_and_set_attributes(self, data: Dict[str, Any]):
        for key, value in data.items():
            self.__setattr__(key, value)

    def validate_dict(self, value: Any, allowed_keys: Set[str]):
        if not isinstance(value, dict):
            raise ValueError(
                    f"Expected a dictionary but got {type(data).__name__}")
        value_keys = set(value.keys())
        unallowed_keys = value_keys.difference(allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s): " +
                             f"{', '.join(unallowed_keys)}")

    @property
    def manifestVersion(self) -> str:
        return self._data["manifestVersion"]

    @manifestVersion.setter
    def manifestVersion(self, value: str):
        if not isinstance(value, str):
            raise ValueError("manifestVersion must be a string")
        self._data["manifestVersion"] = value

    @property
    def package(self) -> Dict[str, Any]:
        return self._data["package"]

    @package.setter
    def package(self, value: Dict[str, Any]):
        allowed_keys = {'name', 'version', 'description', 'authors'}
        try:
            self.validate_dict(value, allowed_keys)
        except ValueError as e:
            raise ValueError(
                    "package must be a dictionary with allowed " +
                    f"keys: {', '.join(allowed_keys)}"
                    ) from e
        self._data["package"] = value

    @property
    def code(self) -> List[Dict[str, Any]]:
        return self._data["code"]

    @code.setter
    def code(self, value: List[Dict[str, Any]]):
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise ValueError("code must be a list of dictionaries")
        self._data["code"] = value

    @property
    def datasets(self) -> List[Dict[str, Any]]:
        return self._data["datasets"]

    @datasets.setter
    def datasets(self, value: List[Dict[str, Any]]):
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise ValueError("datasets must be a list of dictionaries")
        self._data["datasets"] = value

    @property
    def docs(self) -> List[Dict[str, Any]]:
        return self._data["docs"]

    @docs.setter
    def docs(self, value: List[Dict[str, Any]]):
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise ValueError("docs must be a list of dictionaries")
        self._data["docs"] = value

    @property
    def model(self) -> Dict[str, Any]:
        return self._data["model"]

    @model.setter
    def model(self, value: Dict[str, Any]):
        required_keys = {'name', 'path', 'description', 'framework', 'license', 'version', 'parts', 'parameters'}
        if not isinstance(value, dict) or not all(key in value for key in required_keys):
            raise ValueError(f"model must be a dictionary with keys: {required_keys}")
        self._data["model"] = value

    # Serialize to YAML
    def to_yaml(self) -> str:
        return yaml.dump(data = self._data, sort_keys=False,
                         default_flow_style=False)

    # Deserialize from YAML
    # @classmethod
    # def from_yaml(cls, yaml_str: str):
    #     data = yaml.safe_load(yaml_str)
    #     return cls(**data)

# Usage
path = 'modelkit/tests/fixtures/Kitfile_full'
kitfile = Kitfile(path=path)

print("kitfile.manifestVersion: " + kitfile.manifestVersion)
print("kitfile.package: ")
print(kitfile.package)
print("=======================================================")

# Serialize to YAML
yaml_data = kitfile.to_yaml()
print(yaml_data)
print("=======================================================")


kitfile.manifestVersion = "2.0"
kitfile.package = {
    "name": "New-Package",
    "version": "2.0.0",
    "description": "New description",
    "authors": ["Author"]
}

print("kitfile.manifestVersion: " + kitfile.manifestVersion)
print("kitfile.package: ")
print(kitfile.package)
print("=======================================================")
# Serialize to YAML
yaml_data = kitfile.to_yaml()
print(yaml_data)
print("=======================================================")

# Create an empty Kitfile and update attributes
kitfile = Kitfile()
kitfile.manifestVersion = "3.0"
kitfile.package = {
    "name": "Another-Package",
    "version": "3.0.0",
    "description": "Another description",
    "authors": ["Someone"]
}
# Deserialize from YAML
# new_kitfile = Kitfile.from_yaml(yaml_data)
# print("new_kitfile.manifestVersion: " + new_kitfile.manifestVersion)
# print("new_kitfile.package: ")
# print(new_kitfile.package)
