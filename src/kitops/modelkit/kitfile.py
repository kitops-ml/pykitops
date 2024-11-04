import yaml
from pathlib import Path
from typing import Any, Dict, List, Set

from .validators.code_validator import CodeValidator
from .validators.datasets_validator import DatasetsValidator
from .validators.docs_validator import DocsValidator
from .validators.manifest_version_validator import ManifestVersionValidator
from .validators.package_validator import PackageValidator
from .validators.model_validator import ModelValidator


class Kitfile:
    """
    Kitfile class to manage KitOps ModelKits and Kitfiles.

    Attributes:
        path (str): Path to the Kitfile.
    """

    def __init__(self, path=None):
        """
        Initialize the Kitfile.

        Args:
            path (str, optional): Path to the Kitfile. Defaults to None.
        """
        self._data = {}
        self._kitfile_allowed_keys = {'manifestVersion', 'package', 
                                     'code', 'datasets', 'docs', 'model'}
        
        # initialize the kitfile section validators
        self.initialize_kitfile_section_validators()

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

    def initialize_kitfile_section_validators(self):
        """
        Initialize validators for Kitfile sections.
        """
        self._manifestVersion_validator = ManifestVersionValidator(
                                            section='manifestVersion',
                                            allowed_keys=set())
        self._package_validator = PackageValidator(
                                    section='package',
                                    allowed_keys={"name", "version", 
                                                  "description", "authors"})
        self._code_validator = CodeValidator(
                                    section='code',
                                    allowed_keys={"path", "description", 
                                                  "license"})
        self._datasets_validator = DatasetsValidator(
                                    section='datasets',
                                    allowed_keys={"name", "path", 
                                                  "description", "license"})
        self._docs_validator = DocsValidator(
                                    section='docs',
                                    allowed_keys={"path", "description"})
        self._model_validator = ModelValidator(
                                    section='model',
                                    allowed_keys={"name", "path", "framework",
                                                  "version", "description", 
                                                  "license", "parts", 
                                                  "parameters"})

    def load_from_file(self, path):
        """
        Load Kitfile data from a file.

        Args:
            path (str): Path to the Kitfile.
        """
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
        """
        Validate and set attributes from the provided data.

        Args:
            data (Dict[str, Any]): Data to validate and set.
        """
        for key, value in data.items():
            self.__setattr__(key, value)

    def validate_dict(self, value: Any, allowed_keys: Set[str]):
        """
        Validate a dictionary against allowed keys.

        Args:
            value (Any): Value to validate.
            allowed_keys (Set[str]): Set of allowed keys.
        """
        if not isinstance(value, dict):
            raise ValueError(
                    f"Expected a dictionary but got {type(value).__name__}")
        value_keys = set(value.keys())
        unallowed_keys = value_keys.difference(allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s): " +
                             f"{', '.join(unallowed_keys)}")

    @property
    def manifestVersion(self) -> str:
        """
        Get the manifest version.

        Returns:
            str: Manifest version.
        """
        return self._data["manifestVersion"]

    @manifestVersion.setter
    def manifestVersion(self, value: str):
        """
        Set the manifest version.

        Args:
            value (str): Manifest version.
        """
        self._manifestVersion_validator.validate(data=value)
        self._data["manifestVersion"] = value

    @property
    def package(self) -> Dict[str, Any]:
        """
        Get the package information.

        Returns:
            Dict[str, Any]: Package information.
        """
        return self._data["package"]

    @package.setter
    def package(self, value: Dict[str, Any]):
        """
        Set the package information.

        Args:
            value (Dict[str, Any]): Package information.
        """
        self._package_validator.validate(data=value)
        self._data["package"] = value

    @property
    def code(self) -> List[Dict[str, Any]]:
        """
        Get the code section.

        Returns:
            List[Dict[str, Any]]: Code section.
        """
        return self._data["code"]

    @code.setter
    def code(self, value: List[Dict[str, Any]]):
        """
        Set the code section.

        Args:
            value (List[Dict[str, Any]]): Code section.
        """
        self._code_validator.validate(data=value)
        self._data["code"] = value

    @property
    def datasets(self) -> List[Dict[str, Any]]:
        """
        Get the datasets section.

        Returns:
            List[Dict[str, Any]]: Datasets section.
        """
        return self._data["datasets"]

    @datasets.setter
    def datasets(self, value: List[Dict[str, Any]]):
        """
        Set the datasets section.

        Args:
            value (List[Dict[str, Any]]): Datasets section.
        """
        self._datasets_validator.validate(data=value)
        self._data["datasets"] = value

    @property
    def docs(self) -> List[Dict[str, Any]]:
        """
        Get the docs section.

        Returns:
            List[Dict[str, Any]]: Docs section.
        """
        return self._data["docs"]

    @docs.setter
    def docs(self, value: List[Dict[str, Any]]):
        """
        Set the docs section.

        Args:
            value (List[Dict[str, Any]]): Docs section.
        """
        self._docs_validator.validate(data=value)
        self._data["docs"] = value

    @property
    def model(self) -> Dict[str, Any]:
        """
        Get the model section.

        Returns:
            Dict[str, Any]: Model section.
        """
        return self._data["model"]

    @model.setter
    def model(self, value: Dict[str, Any]):
        """
        Set the model section.

        Args:
            value (Dict[str, Any]): Model section.
        """
        self._model_validator.validate(data=value)
        self._data["model"] = value

    def to_yaml(self) -> str:
        """
        Serialize the Kitfile to YAML format.

        Returns:
            str: YAML representation of the Kitfile.
        """
        return yaml.dump(data = self._data, sort_keys=False,
                         default_flow_style=False)
