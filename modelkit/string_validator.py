from typing import Any, Dict, List, Set

class StringValidator:
    def __init__(self, section: str, allowed_keys:Set[str]):
        self.section = section
        self.allowed_keys = allowed_keys

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def allowed_keys(self):
        return self._allowed_keys

    @allowed_keys.setter
    def allowed_keys(self, values):
        self._allowed_keys = values

    def validate(self, data: Any):
        if not isinstance(data, str):
            raise TypeError(f"Expected a string but got {type(data).__name__}")
        # data = data.strip()
        # if not data:
        #     raise ValueError(f"String value must be non-empty.")
