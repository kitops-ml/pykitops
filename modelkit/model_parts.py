from .utils import is_valid_string

class ModelPartsEntry(dict):
    _required_keys = {'path'}
    _optional_keys = {'name', 'type'}
    _allowed_keys = _required_keys.union(_optional_keys)

    def __init__(self, path: str, name: str | None = None,
                 type: str | None = None):
        super().__init__()
        self["path"] = path
        if name is not None:
            self["name"] = name
        if type is not None:
            self["type"] = type

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. " +
                f"Allowed keys are: {', '.join(self._allowed_keys)}")
        
        # The key is allowed.
        # Check if the key is required
        if key in self._required_keys:
            if not is_valid_string(value):
                raise ValueError(
                    f"Key '{key}' must have a non-empty, " + 
                    "non-whitespace string value")

        # Otherwise, the key is optional, so we don't have to be 
        # vigilant about its value       
        super().__setitem__(key, value)

class ModelPartsSectionDict(dict[str, list]):
    _allowed_keys = ['parts']

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. " +
                f"Allowed keys are: {', '.join(self.allowed_keys)}")
        # The key is allowed. Make sure its corresponding value "
        # is a list.
        if not isinstance(value, list):
            raise ValueError(f"Key '{key}' must have a list value")
        # The key is allowed and its corresponding value is a 
        # valid dictionary
        super().__setitem__(key, value)

class ModelPartsSection:
    def __init__(self, entries: list[ModelPartsEntry] | None = None):
        self._modelparts_section = ModelPartsSectionDict()
        self.entries = entries

    @property
    def entries(self) -> list[ModelPartsEntry] | None:
        return self._entries
    
    @entries.setter
    def entries(self, 
                modelparts_entries: list[ModelPartsEntry] | None
    ) -> None:
        if modelparts_entries is None:
            self._entries = []
        else:
            self._entries = modelparts_entries
        
    def add_entry(self, entry: ModelPartsEntry):
        self._entries.append(entry)

    def build(self) -> ModelPartsSectionDict:
        self._modelparts_section["parts"] = self._entries
        return self._modelparts_section
