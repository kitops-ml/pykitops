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

from typing import Any, Dict, Set

def validate_dict(value: Dict[str, Any], allowed_keys: Set[str]):
    """
    Validate a dictionary against allowed keys.

    Examples:
        >>> validate_dict({"a": 1, "b": 2}, {"a", "b"})
        None

        >>> validate_dict({"a": 1, "b": 2}, {"a"})
        ValueError: Found unallowed key(s): b

        >>> validate_dict({"a": 1, "d": 2}, {"a", "b", "c"})
        ValueError: Found unallowed key(s): d

    Args:
        value (Dict[str, Any]): Value to validate.
        allowed_keys (Set[str]): Set of allowed keys.
    """
    if not isinstance(value, dict):
        raise ValueError(
                f"Expected a dictionary but got {type(value).__name__}")
    value_keys = set(value.keys())
    unallowed_keys = value_keys.difference(allowed_keys) 
    if len(unallowed_keys) > 0:
        raise ValueError("Found unallowed key(s): " +
                         f"{', '.join(unallowed_keys)}")

def clean_empty_items(d: Any) -> Any:
    """
    Remove empty items from a dictionary or list.

    Examples:
        >>> clean_empty_items({"a": "", "b": "c", "d": None})
        {'b': 'c'}

        >>> clean_empty_items(["", "a", None])
        ['a']
    
    Args:
        d (Any): Dictionary or list to clean.

    Returns:
        Any: Cleaned dictionary or list.
    """
    if isinstance(d, dict):
        cleaned_dict = {}
        for k, v in d.items():
            if k.strip() and v is not None:
                if isinstance(v, (dict, list)):
                    cleaned_v = clean_empty_items(v)
                    if cleaned_v:  # Only add non-empty items
                        cleaned_dict[k] = cleaned_v
                elif isinstance(v, str) and v.strip() != "":
                    cleaned_dict[k] = v
                elif not isinstance(v, str):
                    cleaned_dict[k] = v
        return cleaned_dict

    elif isinstance(d, list):
        cleaned_list = []
        for item in d:
            if item is not None:
                if isinstance(item, (dict, list)):
                    cleaned_item = clean_empty_items(item)
                    if cleaned_item:  # Only add non-empty items
                        cleaned_list.append(cleaned_item)
                elif isinstance(item, str) and item.strip() != "":
                    cleaned_list.append(item)
                elif not isinstance(item, str):
                    cleaned_list.append(item)
        return cleaned_list

    return d