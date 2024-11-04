from typing import Any, Set
from .string_validator import StringValidator

class DictValidator(StringValidator):
    def __init__(self, section: str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, dict):
            raise TypeError(
                    f"Problem with '{self.section}' section. " +
                    f"Expected a dictionary but got {type(data).__name__}")
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError(
                    f"Problem with '{self.section}' section. " +
                    "Found unallowed key(s): " +
                    f"{', '.join(unallowed_keys)}. " +
                    f"Allowed keys are: {', '.join(self.allowed_keys)}.")

        # the keys are allowed, so process the keys' values
        self.validate_values(data, keys = data_keys) 

    def validate_values(self, data:Any, keys:Set[str]):
        # process the keys in this dict since they're allowed
        for key in keys:
            try:
                super().validate(data[key])
            except ValueError as e:
                raise ValueError(
                        "Problem processing " +
                        f"'{self.section}.[{key}]'.") from e