class KitfileSection:
    def __init__(self, name: str):
        self.name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value