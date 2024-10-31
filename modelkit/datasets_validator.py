from typing import Any, Set
from .dict_list_validator import DictListValidator

class DatasetsValidator(DictListValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        super().validate(data)