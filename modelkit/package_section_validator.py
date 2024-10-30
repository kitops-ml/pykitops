from typing import Any, List, Set
from .dict_section_validator import DictSectionValidator
from .string_section_validator import StringSectionValidator

class PackageValidator(DictSectionValidator):
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
                        StringSectionValidator.validate(self, data=author)
                    except ValueError as e:
                        raise ValueError(
                                "Problem processing list of " +
                                f"'{self._sectionsection}[{key}]'.") from e
            else:
                try:
                    StringSectionValidator.validate(self, data=data[key])
                except ValueError as e:
                    raise ValueError(
                                "Problem processing " +
                                f"'{self._section}[{key}]'.") from e
