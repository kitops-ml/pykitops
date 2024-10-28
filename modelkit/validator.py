import yaml
from typing import Any, Dict, List, Set

class Validator:
    def __init__(self, allowed_keys):
        self.allowed_keys = allowed_keys
    
    def validate_string(self, data: Any):
        if not isinstance(data, str):
            raise ValueError(f"Expected a string but got {type(data).__name__}")
        if not data.strip():
            raise ValueError(f"String value must be non-empty.")

class StringValidator(Validator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate_string(data)

class DictValidator(StringValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, dict):
            raise ValueError(
                    f"Expected a dictionary but got {type(data).__name__}")
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s): " +
                             f"{', '.join(unallowed_keys)}")
            
        # process the keys in this dict since they're allowed
        for key in data_keys:
            super().validate_string(data[key])

class DictListValidator(DictValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, list):
            raise ValueError(f"Expected a list but got {type(data).__name__}")

        # process the list of items
        for item in data:
            super().validate(item)

class NestedDictsValidator(Validator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, dict):
            raise ValueError(f"Expected a dictionary but got {type(data).__name__}")

class ManifestVersionValidator(StringValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
            super().validate(data)

class PackageValidator(NestedDictsValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)

        # raise an error if data contains any keys other than
        # those which are allowed
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys)   
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s) in 'package': " +
                             f"{', '.join(unallowed_keys)}")
        
        # the keys in data are allowed, so process their values
        for key in data_keys:
            if key == 'authors':
                if not isinstance(data[key], list):
                    raise ValueError("Expected a list for 'package[authors]'")
                # authors is a list
                for author in data[key]:
                    super().validate_string(author)
            else:
                super().validate_string(data[key])

class CodeValidator(DictListValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)

class DatasetsValidator(DictListValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)

class DocsValidator(DictListValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)

class ModelPartsValidator(DictListValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)
    
class ModelValidator(NestedDictsValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

        self.parts_validator_map = {
            'parts': 
                ModelPartsValidator(
                    allowed_keys={'name', 'path', 'type'}),
        }

    def validate(self, data: Any):
        super().validate(data)

        # raise an error if data contains any keys other than
        # those which are allowed
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys)   
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s) in 'model': " +
                             f"{', '.join(unallowed_keys)}")
        
        # the keys in data are allowed, so process their values
        for key in data_keys:
            if key == 'parts':
                self.parts_validator_map[key].validate(data[key])
            elif key == 'parameters':
                # the 'parameters' section can be any valid YAML
                # content, so presumably any YAML-related errors
                # would have been raised when the content was
                # read from the input stream; no further
                # processing should be necessary
                continue
            else:
                # all other values just need to be confirmed as
                # being valid strings
                super().validate_string(data[key])

# Kitfile validator
class KitfileValidator(NestedDictsValidator):
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

        # raise an error if data contains keys other
        # than those allowed
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys)
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s): " +
                             f"{', '.join(unallowed_keys)}")
        
        # the keys present in the dictionary are allowed so 
        # validate their corresponding values individually
        for key in data_keys:
            self.validator_map[key].validate(data[key])
            # eval(self._validator_map[key].validate(data[key]))


# Usage

yaml_data = """
manifestVersion: "1.0"
package:
  name: "Titanic-Survivability-Predictor"
  version: "1.0.0"
  description: "A model attempting to predict passenger survivability of the Titanic Shipwreck"
  authors:
    - "Jozu"
code:
  - path: "requirements.txt"
    description: "Python packages required by this example."
    license: "Apache-2.0"
  - path: "titanic_survivability.ipynb"
    description: "Jupyter Notebook used to train, validate, optimize and export the model."
    license: "Apache-2.0"
datasets:
  - name: "training"
    path: "data/train.csv"
    description: "Data to be used for model training."
    license: "Apache-2.0"
  - name: "testing"
    path: "data/test.csv"
    description: "Data to be used for model testing."
    license: "Apache-2.0"
docs:
  - path: "README.md"
    description: "Important notes about the project."
  - path: "images"
    description: "Directory containing figures and graphs exported as image files."
model:
  name: "titanic-survivability-predictor"
  path: "model"
  description: "Directory containing figures and graphs exported as image files."
  framework: "joblib"
  license: "Apache-2.0"
  version: "1.0"
  parts:
    - path: "config.json"
      name: "config"
      type: "config file"
    - path: "tokenizer.json"
    - path: "tokenizer_config.json"
    - path: "vocab.txt"
  parameters:
    param1: "val1"
    param2: "val2"
    items:
      - "list item 1"
      - "list item 2"
"""

# Load and validate
data = yaml.safe_load(yaml_data)
validator = KitfileValidator()
validator.validate(data)