from .utils import is_valid_string

class CodeEntry(dict):
    _required_keys = {'path'}
    _optional_keys = {'description', 'license'}
    _allowed_keys = _required_keys.union(_optional_keys)

    def __init__(self, path: str, description: str | None = None, 
                 license: str | None = None):
        super().__init__()
        self["path"] = path
        if description is not None:
            self["description"] = description
        if license is not None:
            self["license"] = license

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(f"Key '{key}' is not allowed. Allowed keys are: {', '.join(self._allowed_keys)}")
        
        # The key is allowed.
        # Check if the key is required
        if key in self._required_keys:
            if not is_valid_string(value):
                raise ValueError(f"Key '{key}' must have a non-empty, non-whitespace string value")

        # Otherwise, the key is optional, so we don't have to be 
        # vigilant about its value       
        super().__setitem__(key, value)

class CodeSectionDict(dict[str, list]):
    _allowed_keys = ['code']

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(f"Key '{key}' is not allowed. Allowed keys are: {', '.join(self.allowed_keys)}")
        # The key is allowed. Make sure its corresponding value is a list.
        if not isinstance(value, list):
            raise ValueError(f"Key '{key}' must have a list value")
        # The key is allowed and its corresponding value is a valid dictionary
        super().__setitem__(key, value)

class CodeSection:
    def __init__(self, entries: list[CodeEntry] | None = None):
        self._code_section = CodeSectionDict()
        if entries is None:
            self._entries = []
        else:
            self._entries = entries

    @property
    def entries(self) -> list[CodeEntry]:
        return self._entries
    
    @entries.setter
    def entries(self, code_entries: list[CodeEntry]) -> None:
        if code_entries is None:
            self._entries = []
        else:
            self._entries = code_entries
        
    def add_entry(self, entry: CodeEntry):
        self._entries.append(entry)

    def build(self) -> CodeSectionDict:
        self._code_section["code"] = self._entries
        return self._code_section

