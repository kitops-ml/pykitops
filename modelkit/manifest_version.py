from typing import Any, Dict, Set
from .utils import is_empty_string
from .base_validators import StringValidator
from .kitfile_section import KitfileSection

class ManifestVersionSection(KitfileSection):
    def __init__(self, data: str):
        super().__init__(section_name='manifestVersion', allowed_keys=set())
        self._data: Dict[str, str] = {self.section_name: ""}
        self._validator = StringValidator(self.allowed_keys)
        self.manifest_version = data

    @property
    def manifest_version(self) -> str:
        return self._data[self.section_name]
    
    @manifest_version.setter
    def manifest_version(self, data: str) -> None:
        try:
            self._data[self.section_name] = self._validator.validate(data)
        except ValueError as e:
            raise ValueError("Invalid 'manifestVersion'.") from e
        self._manifest_version = self.validate(data)
