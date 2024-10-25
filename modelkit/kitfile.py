import yaml
from pathlib import Path
from .manifest_version import ManifestVersionSection
from .package import (
    PackageSection,
    PackageEntry
)
from .code import (
    CodeSection, 
    CodeEntry
)
from .datasets import (
    DatasetsSection, 
    DatasetsEntry
)
from .docs import (
    DocsSection, 
    DocsEntry
)
from .model_parts import (
    ModelPartsSection,
    ModelPartsSectionDict,
    ModelPartsEntry
)
from .model import (
    ModelSection, 
    ModelEntry
)
from .utils import (
    is_empty_list,
    custom_dict_representer
)

# class NoTagsDumper(yaml.SafeDumper):
#     def ignore_aliases(self, data):
#         return True

class Kitfile:
    def __init__(self):
        self._manifest_version_section = None
        self._package_section = None
        self._code_section = None
        self._datasets_section = None
        self._docs_section = None
        self._model_section = None

    @property
    def manifest_version_section(self):
        return self._manifest_version_section
    
    @manifest_version_section.setter
    def manifest_version_section(self, value: ManifestVersionSection):
        self._manifest_version_section = value
            
    @property
    def package_section(self):
        return self._package_section
    
    @package_section.setter
    def package_section(self, value: PackageSection):
        self._package_section = value

    @property
    def code_section(self):
        return self._code_section
    
    @code_section.setter
    def code_section(self, value: CodeSection):
        self._code_section = value

    @property
    def datasets_section(self):
        return self._datasets_section
    
    @datasets_section.setter
    def datasets_section(self, value: DatasetsSection):
        self._datasets_section = value

    @property
    def docs_section(self):
        return self._docs_section
    
    @docs_section.setter
    def docs_section(self, value: DocsSection):
        self._docs_section = value

    @property
    def model_section(self):
        return self._model_section
    
    @model_section.setter
    def model_section(self, value: ModelSection):
        self._model_section = value

    def build(self) -> str:
        self._data = {}
        self._data.update(self._manifest_version_section.build())
        self._data.update(self._package_section.build())
        if (self._code_section is not None and
            not is_empty_list(self._code_section.entries)):
            self._data.update(self._code_section.build())
        if (self._datasets_section is not None and
            not is_empty_list(self._datasets_section.entries)):
            self._data.update(self._datasets_section.build())
        if (self._docs_section is not None and
            not is_empty_list(self._docs_section.entries)):
            self._data.update(self._docs_section.build())
        if self._model_section is not None:
            self._data.update(self._model_section.build())

        yaml.add_representer(PackageEntry, custom_dict_representer)
        yaml.add_representer(CodeEntry, custom_dict_representer)
        yaml.add_representer(DatasetsEntry, custom_dict_representer)
        yaml.add_representer(DocsEntry, custom_dict_representer)
        yaml.add_representer(ModelPartsEntry, custom_dict_representer)
        yaml.add_representer(ModelPartsSectionDict, custom_dict_representer)
        yaml.add_representer(ModelEntry, custom_dict_representer)

        return yaml.dump(data = self._data, sort_keys=False)
    
