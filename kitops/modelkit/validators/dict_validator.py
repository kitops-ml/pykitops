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

from typing import Any, Set
from .string_validator import StringValidator

class DictValidator(StringValidator):
    def __init__(self, section: str, allowed_keys:Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, dict):
            raise TypeError(
                    f"Problem with '{self.section}' section. " +
                    f"Expected a dictionary but got {type(data).__name__}")
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self.allowed_keys) 
        if len(unallowed_keys) > 0:
            raise ValueError(
                    f"Problem with '{self.section}' section. " +
                    "Found unallowed key(s): " +
                    f"{', '.join(unallowed_keys)}. " +
                    f"Allowed keys are: {', '.join(self.allowed_keys)}.")

        # the keys are allowed, so process the keys' values
        self.validate_values(data, keys = data_keys) 

    def validate_values(self, data:Any, keys:Set[str]):
        # process the keys in this dict since they're allowed
        for key in keys:
            try:
                super().validate(data[key])
            except ValueError as e:
                raise ValueError(
                        "Problem processing " +
                        f"'{self.section}.[{key}]'.") from e