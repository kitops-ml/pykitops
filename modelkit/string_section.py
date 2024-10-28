from .kitfile_section import KitfileSection

class StringSection(KitfileSection):
    def __init__(self, name:str, value:str):
        super().__init__(name)
        self.string = value

    @property
    def string(self) -> str:
        return self._string
    
    @string.setter
    def string(self, value) -> None:
        self._string = value
    