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

from typing import Any, List, Set
from .dict_validator import DictValidator
from .string_validator import StringValidator

class PackageValidator(DictValidator):
    def __init__(self, section:str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        super().validate(data)
        
    # Overrides DictValidator.validate_values
    def validate_values(self, data, keys):
        # the keys in data are allowed, so process their values
        for key in keys:
            if key == 'authors':
                if not isinstance(data[key], list):
                    raise ValueError(
                            "Expected a list for " + 
                            f"'{self._section}[{key}]'")
                # authors is a list
                for author in data[key]:
                    try:
                        StringValidator.validate(self, data=author)
                    except ValueError as e:
                        raise ValueError(
                                "Problem processing list of " +
                                f"'{self._sectionsection}[{key}]'.") from e
            else:
                try:
                    StringValidator.validate(self, data=data[key])
                except ValueError as e:
                    raise ValueError(
                                "Problem processing " +
                                f"'{self._section}[{key}]'.") from e
