from .restricted_dict import RestrictedDict
from .utils import is_valid_string, is_valid_list, is_empty_list

class PackageSection:
    _section_name = 'package'
    _string_valued_keys = {'name', 'version', 'description'}
    _list_valued_keys = {'authors'}

    def __init__(self, name: str | None, version: str | None, 
                 description: str | None = None, 
                 authors: list[str] | None = None,
                 data: dict | None = None):
        self._package_entry = \
            RestrictedDict(name="package body",
                string_valued_keys = self._string_valued_keys,
                list_valued_keys = self._list_valued_keys, data = data)
        self._package_section = \
            RestrictedDict(name="package section",
                string_valued_keys={self._section_name})
        if not data:
            self.name = name
            self.version = version
            if description:
                self.description = description
            if authors:
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

    def build(self) -> RestrictedDict:
        # filter out any of the Package contents that are None
        # or are empty
        # package = {k: v for k, v in self._package_entry.items() 
        #               if (isinstance(k, str) and v not in (None, "")) or 
        #                  (isinstance(k, list) and not is_empty_list(v))}
        # self._package_section["package"] = package
        self._package_section["package"] = self._package_entry
        return self._package_section
