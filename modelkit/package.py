from .utils import is_valid_string, is_valid_list, is_empty_list

class PackageEntry(dict):
    _required_keys = {'name', 'version'}
    _optional_keys = {'description', 'authors'}
    _allowed_keys = _required_keys.union(_optional_keys)
    _keys_with_string_values = {'name', 'version', 'description'}
    _keys_with_list_values = {'authors'}

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. " +
                f"Allowed keys are: {', '.join(self._allowed_keys)}")
        
        # The key is allowed.
        # Check if the key is required
        if key in self._required_keys:
            if key in self._keys_with_string_values:
                if not is_valid_string(value):
                    raise ValueError(
                        f"Key '{key}' must have a non-empty, " +
                        "non-whitespace string value")
            if key in self._keys_with_list_values:
                if not is_valid_list(value):
                    raise ValueError(
                        f"Key '{key}' must be a non-empty list")

        # Otherwise, the key is optional, so we don't have to be 
        # vigilant about its value       
        super().__setitem__(key, value)

class PackageSectionDict(dict):
    _allowed_keys = ['package']

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. " +
                "Allowed keys are: {', '.join(self.allowed_keys)}")
        # The key is allowed. Make sure its corresponding value is 
        # a dictionary.
        if not isinstance(value, dict):
            raise ValueError(
                f"Key '{key}' must have a dictionary value")
        # The key is allowed and its corresponding value is a 
        # valid dictionary
        super().__setitem__(key, value)

class PackageSection:
    def __init__(self, name: str | None, version: str | None, 
                 description: str | None = None, 
                 authors: list[str] | None = None):
        self._package_section =  PackageSectionDict()
        self._package_entry = PackageEntry()
        self.name = name
        self.version = version
        if description is not None:
            self.description = description
        if authors is not None:
            self.authors = authors

    @property
    def name(self) -> str | None:
        return self._package_entry["name"]

    @name.setter
    def name(self, value: str | None) -> None:
        self._package_entry["name"] = value

    @property
    def version(self) -> str | None:
        return self._package_entry["version"]
    
    @version.setter
    def version(self, value: str | None) -> None:
        self._package_entry["version"] = value

    @property
    def description(self) -> str | None:
        return self._package_entry["description"]
    
    @description.setter
    def description(self, value: str) -> None:
        self._package_entry["description"] = value

    @property
    def authors(self) -> list[str] | None:
        return self._package_entry["authors"]
    
    @authors.setter
    def authors(self, list: list[str] | None) -> None:
        self._package_entry["authors"] = list

    def build(self) -> PackageSectionDict:
        # filter out any of the Package contents that are None
        # or are empty
        # package = {k: v for k, v in self._package_entry.items() 
        #               if (isinstance(k, str) and v not in (None, "")) or 
        #                  (isinstance(k, list) and not is_empty_list(v))}
        # self._package_section["package"] = package
        self._package_section["package"] = self._package_entry
        return self._package_section
    
    @classmethod
    def create_from_yaml(cls, data):
        if data:
            # iterate through the section's allowed keys
            provided_keys = set(data.keys())
            matchin_keys = provided_keys.intersection(
                                PackageSection._all
            )
        else:
            package_section =PackageSection()