'''
Copyright 2024 The KitOps Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
'''

from typing import Any, Dict, List, Set
from .dict_list_validator import DictListValidator
from .dict_validator import DictValidator
from .string_validator import StringValidator

class ModelPartsValidator(DictListValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        super().validate(data)

class ModelValidator(DictValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

        self._parts_validator = ModelPartsValidator(
                                    section="parts",
                                    allowed_keys={'name', 'path', 'type'})
        
    def validate(self, data: Any):
        super().validate(data)
    
    def validate_values(self, data: Any, keys=Set[str]):
        # the keys in data are allowed, so process their values
        for key in keys:
            if key == 'parts':
                self._parts_validator.validate(data[key])
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
                try:
                    StringValidator.validate(self, data=data[key])
                except ValueError as e:
                    raise ValueError(
                                "Problem processing " +
                                f"'{self._section}[{key}]'.") from e
