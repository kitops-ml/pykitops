from typing import List
from .kitfile_section import KitfileSection

class ListSection(KitfileSection):
    def __init__(self, name:str, value:List):
        super().__init__(name)
        self.list = value

    @property
    def list(self) -> List:
        return self._list
    
    @list.setter
    def list(self, value: List) -> None:
        self._list = value