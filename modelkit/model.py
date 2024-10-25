import yaml
from .model_parts import ModelPartsEntry, ModelPartsSection
from .utils import is_valid_string, is_valid_list, is_empty_list

class ModelEntry(dict):
    _required_keys = {'path'}
    _optional_keys = {'name', 'framework', 'version', 'description', 
                      'license', 'parts', 'parameters'}
    _allowed_keys = _required_keys.union(_optional_keys)
    _keys_with_string_values = {'path', 'name', 'framework',
                                'version', 'description', 'license'}
    _keys_with_model_parts_section_values = {'parts'}
    _keys_with_yaml_values = {'parameters'}

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
            if key in self._keys_with_model_parts_section_values:
                if not isinstance(value, ModelPartsSection):
                    raise TypeError(
                        f"Value '{key}' value must be a " +
                        "ModelPartsSection")
            if key in self._keys_with_yaml_values:
                value = yaml.safe_load(value)
                
        # Otherwise, the key is optional, so we don't have to be 
        # vigilant about its value       
        super().__setitem__(key, value)

class ModelSectionDict(dict):
    _allowed_keys = ['model']

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
    
class ModelSection:
    def __init__(self, path: str, name: str | None = None, 
                 framework: str | None = None, 
                 version: str | None = None, 
                 description: str | None = None, 
                 license: str | None = None,
                 parts: ModelPartsSection | None = None,
                 parameters: str |None = None):
        self._model_section = ModelSectionDict()
        self._model_entry = ModelEntry()
        self.path = path
        if name is not None:
            self.name = name
        if framework is not None:
            self.framework = framework
        if version is not None:
            self.version = version
        if description is not None:
            self.description = description
        if license is not None:
            self.license = license
        if parts is not None:
            self.parts = parts
        if parameters is not None:
            self.parameters = parameters

# class ModelSection:
#     def __init__(self):
#         self._model_section =  ModelSectionDict()
#         self._model_entry = ModelEntry()

    @property
    def path(self) -> str:
        return self._model_entry["path"]
    
    @path.setter
    def path(self, value: str) -> None:
        self._model_entry["path"] = value

    @property
    def name(self) -> str:
        return self._model_entry["name"]

    @name.setter
    def name(self, value: str) -> None:
        self._model_entry["name"] = value

    @property
    def framework(self) -> str:
        return self._model_entry["framework"]

    @framework.setter
    def framework(self, value: str) -> None:
        self._model_entry["framework"] = value

    @property
    def version(self) -> str:
        return self._model_entry["version"]
    
    @version.setter
    def version(self, value: str) -> None:
        self._model_entry["version"] = value

    @property
    def description(self) -> str | None:
        return self._model_entry["description"]
    
    @description.setter
    def description(self, value: str) -> None:
        self._model_entry["description"] = value

    @property
    def license(self) -> str:
        return self._model_entry["license"]

    @license.setter
    def license(self, value: str) -> None:
        self._model_entry["license"] = value

    @property
    def parts(self) -> ModelPartsSection | None:
        return self._model_entry["parts"]

    @parts.setter
    def parts(self, model_parts: ModelPartsSection | None) -> None:
        self._model_entry["parts"] = model_parts

    @property
    def parameters(self) -> str:
        return self._model_entry["parameters"]

    @parameters.setter
    def parameters(self, value: str) -> None:
        self._model_entry["parameters"] = value
    
    def build(self) -> ModelSectionDict:
        # filter out any of the Model contents that are None
        # or are empty
        # model = {k: v for k, v in self._model_entry.items() 
        #               if (isinstance(k, str) and v not in (None, "")) or 
        #                  (isinstance(k, list) and not is_empty_list(v))}
        # self._model_section["model"] = model
        self._model_section["model"] = self._model_entry
        return self._model_section    