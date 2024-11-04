from typing import Any, Set
from .string_validator import StringValidator

class ManifestVersionValidator(StringValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        super().validate(data)