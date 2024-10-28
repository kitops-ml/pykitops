import yaml
from typing import TypeAlias, List, Dict
from pathlib import Path
from .manifest_version import ManifestVersionSection
#from .package import PackageSection, PackageEntry
from .package_alt import PackageSection
from .code import CodeSection, CodeEntry
from .datasets import DatasetsSection, DatasetsEntry
from .docs import DocsSection, DocsEntry
from .model_parts import ModelPartsSectionDict, ModelPartsEntry
from .model import ModelSection, ModelEntry
from .restricted_dict import RestrictedDict
from .utils import is_empty_list, custom_dict_representer

class Kitfile(RestrictedDict):
    _allowed_section_names = {'manifestVersion',
                              'package',
                              'code',
                              'datasets',
                              'docs',
                              'model'}
    
    def __init__(self, data:Dict|None=None):
        super().__init__(name="Kitfile", data=data,
                         string_valued_keys={"manifestVersion"},
                         list_valued_keys={"code","datasets","docs"},
                         dict_valued_keys={"package","model"})
        

        # self._manifest_version_section: ManifestVersionSection | None = None
        # self._package_section: PackageSection | None = None
        # self._code_section: CodeSection | None = None
        # self._datasets_section: DatasetsSection | None = None
        # self._docs_section: DocsSection | None = None
        # self._model_section: ModelSection | None = None
        # try to load the contents of the kitfile from the 
        # data object;
        # return None if the stream isn't provided

    @property
    def manifest_version_section(self) -> ManifestVersionSection:
        return self._manifest_version_section
    
    @manifest_version_section.setter
    def manifest_version_section(self, value: ManifestVersionSection) -> None:
        self._manifest_version_section = value
            
    @property
    def package_section(self) -> PackageSection:
        return self._package_section
    
    @package_section.setter
    def package_section(self, value: PackageSection) -> None:
        self._package_section = value

    @property
    def code_section(self) -> CodeSection:
        return self._code_section
    
    @code_section.setter
    def code_section(self, value: CodeSection) -> None:
        self._code_section = value

    @property
    def datasets_section(self) -> DatasetsSection:
        return self._datasets_section
    
    @datasets_section.setter
    def datasets_section(self, value: DatasetsSection) -> None:
        self._datasets_section = value

    @property
    def docs_section(self) -> DocsSection:
        return self._docs_section
    
    @docs_section.setter
    def docs_section(self, value: DocsSection) -> None:
        self._docs_section = value

    @property
    def model_section(self) -> ModelSection:
        return self._model_section
    
    @model_section.setter
    def model_section(self, value: ModelSection) -> None:
        self._model_section = value

    def build(self) -> str:
        self._data = Dict
        self._data.update(self.manifest_version_section.build())
        self._data.update(self.package_section.build())
        # if (self.code_section is not None and
        #     not is_empty_list(self.code_section.entries)):
        #     self._data.update(self.code_section.build())
        # if (self.datasets_section is not None and
        #     not is_empty_list(self.datasets_section.entries)):
        #     self._data.update(self.datasets_section.build())
        # if (self.docs_section is not None and
        #     not is_empty_list(self.docs_section.entries)):
        #     self._data.update(self.docs_section.build())
        # if self.model_section is not None:
        #     self._data.update(self.model_section.build())

        yaml.add_representer(RestrictedDict, custom_dict_representer)
        #yaml.add_representer(PackageEntry, custom_dict_representer)
        yaml.add_representer(CodeEntry, custom_dict_representer)
        yaml.add_representer(DatasetsEntry, custom_dict_representer)
        yaml.add_representer(DocsEntry, custom_dict_representer)
        yaml.add_representer(ModelPartsEntry, custom_dict_representer)
        yaml.add_representer(ModelPartsSectionDict, custom_dict_representer)
        yaml.add_representer(ModelEntry, custom_dict_representer)

        return yaml.dump(data = self._data, sort_keys=False,
                         default_flow_style=False)
    