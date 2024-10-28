from typing import Dict
from .kitfile_section import KitfileSection

class DictSection(KitfileSection):
    def __init__(self, name:str, value:Dict):
        super().__init__(name)
        self.dict = value

    @property
    def dict(self) -> Dict:
        return self._dict
    
    @dict.setter
    def dict(self, value) -> None:
        self._dict = value
    