from .utils import is_valid_string

class DocsEntry(dict):
    _required_keys = {'path'}
    _optional_keys = {'description'}
    _allowed_keys = _required_keys.union(_optional_keys)

    def __init__(self, path: str, name: str | None = None,
                 description: str | None = None, 
                 license: str | None = None):
        super().__init__()
        self["path"] = path
        if description is not None:
            self["description"] = description

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

class DocsSectionDict(dict[str, list]):
    _allowed_keys = ['docs']

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. " +
                f"Allowed keys are: {', '.join(self.allowed_keys)}")
        # The key is allowed. Make sure its corresponding value 
        # is a list.
        if not isinstance(value, list):
            raise ValueError(f"Key '{key}' must have a list value")
        # The key is allowed and its corresponding value is a 
        # valid dictionary
        super().__setitem__(key, value)

class DocsSection:
    def __init__(self, entries: list[DocsEntry] | None = None):
        self._docs_section = DocsSectionDict()
        if entries is None:
            self._entries = []
        else:
            self._entries = entries

    @property
    def entries(self) -> list[DocsEntry]:
        return self._entries
    
    @entries.setter
    def entries(self, docs_entries: list[DocsEntry]) -> None:
        if docs_entries is None:
            self._entries = []
        else:
            self._entries = docs_entries
        
    def add_entry(self, entry: DocsEntry):
        self._entries.append(entry)

    def build(self) -> DocsSectionDict:
        self._docs_section["docs"] = self._entries
        return self._docs_section

