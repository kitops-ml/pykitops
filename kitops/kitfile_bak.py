import yaml
from typing import TypeAlias, List, Dict
from pathlib import Path
from .base_validators import DictValidator
from .manifest_version import ManifestVersionSection
from .package import PackageSection
from .code import CodeSection, CodeEntry
from .datasets import DatasetsSection, DatasetsEntry
from .docs import DocsSection, DocsEntry
from .model_parts import ModelPartsSectionDict, ModelPartsEntry
from .model import ModelSection, ModelEntry
from .restricted_dict import RestrictedDict
from .utils import is_empty_list, custom_dict_representer

# Kitfile validator
class KitfileValidator(DictValidator):
    def __init__(self, allowed_keys = None):
        self.validator_map = {
            'manifestVersion': 
                ManifestVersionValidator(
                    allowed_keys=set()),
            'package': 
                PackageValidator(
                    allowed_keys={'name', 'version', 'description', 
                                  'authors'}),
            'code': 
                CodeValidator(
                    allowed_keys={'path', 'description', 'license'}),
            'datasets': 
                DatasetsValidator(
                    allowed_keys={'name', 'path', 'description', 
                                  'license'}),
            'docs': 
                DocsValidator(
                    allowed_keys={'path', 'description'}),
            'model': 
                ModelValidator(
                        allowed_keys={'name', 'path', 'description', 
                                      'framework', 'license', 'version', 
                                      'parts', 'parameters'})
        }
        allowed_keys = set(self.validator_map.keys())
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        # raise an error if data isn't a dictionary type
        super().validate(data)

    def validate_values(self, data, keys):
        for key in keys:
            self.validator_map[key].validate(data[key])

class Kitfile:
    def __init__(self, path):
        self._data = {}

        if path:
            self.load_from_file(path)
        else:
            self.initialize_empty_kitfile()

    def load_from_file(self, path):
        kitfile_path = Path(path)
        if not kitfile_path.exists():
            raise ValueError(f"Path '{kitfile_path}' does not exist.")
        
        # try to load the kitfile
        try:
            with open(kitfile_path, 'r') as kitfile:
            # Load the yaml data
                data = yaml.safe_load(kitfile)
        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                raise yaml.YAMLError(
                            "Error parsing Kitfile at " +
                            f"line{mark.line+1}, " +
                            f"column:{mark.column+1}.") from e
            else:
                raise
        # kitfile has been successfully loaded into data
        self.validate_and_set_attributes(data)

    def initialize_empty_kitfile(self):
        self.manifest_version_section = ""
        self.package_section = {}
        self.code_section = []
        self.datasets_section = []
        self.docs_section = {}
        self.model_section = {}

    def validate_and_set_attributes(data):
        # TO DO
        
    
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
    