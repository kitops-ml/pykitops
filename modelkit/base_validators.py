import yaml
from typing import Any, Dict, List, Set

class StringValidator:
    def __init__(self, allowed_keys):
        self.allowed_keys = allowed_keys

    @property
    def allowed_keys(self):
        return self._allowed_keys

    @allowed_keys.setter
    def allowed_keys(self, values):
        self._allowed_keys = values

    def validate(self, data: Any) -> str:
        if not isinstance(data, str):
            raise ValueError(f"Expected a string but got {type(data).__name__}")
        data = data.strip()
        if not data:
            raise ValueError(f"String value must be non-empty.")
        # the string passed validation so return it
        return data
    
class DictValidator(StringValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError(
                    f"Expected a dictionary but got {type(data).__name__}")
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError("Found unallowed key(s): " +
                             f"{', '.join(unallowed_keys)}")

        # the keys are allowed, so process the keys' values
        self.validate_values(data, keys = data_keys) 

    def validate_values(self, data, keys):
        # process the keys in this dict since they're allowed
        for key in keys:
            super().validate(data[key])

class DictListValidator(DictValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, list):
            raise ValueError(f"Expected a list but got {type(data).__name__}")

        # process the list of items
        for item in data:
            super().validate(item)

#  =======================================================================



class PackageValidator(DictValidator):
    def __init__(self, allowed_keys):
        super().__init__(allowed_keys)

    def validate(self, data: Any):
        super().validate(data)
        
    # Overrides DictValidator.validate_values
    def validate_values(self, data, keys):
        # the keys in data are allowed, so process their values
        for key in keys:
            if key == 'authors':
                if not isinstance(data[key], list):
                    raise ValueError("Expected a list for 'package[authors]'")
                # authors is a list
                for author in data[key]:
                    StringValidator.validate(self, data=author)
            else:
                StringValidator.validate(self, data=data[key])

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
    
class ModelValidator(DictValidator):
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
    
    def validate_values(self, data, keys):
        # the keys in data are allowed, so process their values
        for key in keys:
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
                StringValidator.validate(self, data=data[key])


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