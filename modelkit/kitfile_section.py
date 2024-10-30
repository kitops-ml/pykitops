from typing import Set
class KitfileSection:
    def __init__(self, section_name: str, allowed_keys:Set):
        self.section_name = section_name
        self.allowed_keys = allowed_keys
    
    @property
    def section_name(self) -> str:
        return self._section_name
    
    @section_name.setter
    def section_name(self, value: str) -> None:
        self._section_name = value

    @property
    def allowed_keys(self) -> Set:
        return self._allowed_keys
    
    @allowed_keys.setter
    def allowed_keys(self, values: Set) -> None:
        self._allowed_keys = values