from typing import Any, Dict, List, Set
from .utils import is_empty_string
from .base_validators import DictValidator
from .kitfile_section import KitfileSection

class PackageSection(KitfileSection):
    def __init__(self, data: Dict[str, str|List[str]], name: str | None = None, 
                 version: str | None = None, description: str | None = None, 
                 authors: List[str] | None = None):
        section_name = 'package'
        self._data: Dict = {
            section_name: {
                'name': "", 
                'version': "", 
                'description': "", 
                'authors': List[str]
            }
        }
        allowed_keys = self._data[section_name].keys()
        super().__init__(section_name=section_name, allowed_keys=allowed_keys)
        self._validator = DictValidator(allowed_keys)

        # if data is provided, then construct the PackageSection
        # from it; otherwise, create the data dictionary using 
        # the other supplied parameters
        if not data:
            data = dict()
            if name:
                data.update({'name', name})
            if version:
                data.update({'version', version})
            if description:
                data.update({'description', description})
            if authors:
                data.update({'authors', authors})

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