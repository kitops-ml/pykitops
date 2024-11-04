from typing import Any, List, Set
from .dict_validator import DictValidator
from .string_validator import StringValidator

class PackageValidator(DictValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        super().validate(data)
        
    # Overrides DictValidator.validate_values
    def validate_values(self, data, keys):
        # the keys in data are allowed, so process their values
        for key in keys:
            if key == 'authors':
                if not isinstance(data[key], list):
                    raise ValueError(
                            "Expected a list for " + 
                            f"'{self._section}[{key}]'")
                # authors is a list
                for author in data[key]:
                    try:
                        StringValidator.validate(self, data=author)
                    except ValueError as e:
                        raise ValueError(
                                "Problem processing list of " +
                                f"'{self._sectionsection}[{key}]'.") from e
            else:
                try:
                    StringValidator.validate(self, data=data[key])
                except ValueError as e:
                    raise ValueError(
                                "Problem processing " +
                                f"'{self._section}[{key}]'.") from e
