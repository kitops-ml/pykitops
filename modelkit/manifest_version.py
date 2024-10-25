from .utils import is_empty_string

"""
Defines a dictionary that can only have a single key named
'manifestVersion', whose corresponding value must be a string.
"""
class ManifestVersionDict(dict):
    _allowed_keys = {'manifestVersion'}

    def __setitem__(self, key, value):
        # Make sure the given key is allowed.
        if key not in self._allowed_keys:
            raise KeyError(f"Key '{key}' is not allowed. Allowed keys are: {', '.join(self.allowed_keys)}")
        # The key is allowed. Make sure its corresponding value is
        # a string
        if not isinstance(value, str) or is_empty_string(value):
            raise ValueError(f"Key '{key}' must have a string value that is non-empty and not comprised soley of whitespace characters")
        # The key is allowed and its corresponding value is a valid string
        # so add it to the dictionary.
        super().__setitem__(key, value)


class ManifestVersionSection:
    def __init__(self, version: str = '1.0'):
        self._manifest_version_section = ManifestVersionDict()
        self.version = version

    @property
    def version(self) -> str:
        return self._manifest_version_section["manifestVersion"]
    
    @version.setter
    def version(self, value: str) -> None:
        self._manifest_version_section["manifestVersion"] = value


    def build(self) -> ManifestVersionDict:
        return self._manifest_version_section