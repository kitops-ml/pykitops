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
import enum
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Dict, Set

class Color(enum.Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

IS_A_TTY = sys.stdout.isatty()

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

def get_or_create_directory(directory: str) -> str:
    """
    Get or create a directory.

    Examples:
        >>> get_or_create_directory("my-directory")
        "my-directory"

    Args:
        directory (str): Directory to get or create.

    Returns:
        str: The directory.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path.as_posix()

def parse_modelkit_tag(tag: str) -> Dict[str, str]:
    """
    Parse a ModelKit tag into its components.

    Examples:
        >>> parse_modelkit_tag("jozu.ml/jozu-demos/titanic-survivability:latest")
        {
            "registry": "jozu.ml",
            "namespace": "jozu-demos",
            "model": "titanic-survivability",
            "tag": "latest"
        }

    Args:
        tag (str): Tag to parse.

    Returns:
        Dict[str, str]: Parsed components of the tag.
    """
    parts = tag.split("/")
    if len(parts) != 3 or ":" not in parts[2]:
        raise ValueError(f"Invalid tag format: {tag}")
    return {
        "registry": parts[0],
        "namespace": parts[1],
        "model": parts[2].split(":")[0],
        "tag": parts[2].split(":")[1]
    }

def load_environment_variables() -> Dict[str, str | None]:
    load_dotenv(override=True)
    username = os.getenv("JOZU_USERNAME")
    password = os.getenv("JOZU_PASSWORD")
    if not username or not password:
        raise ValueError("Missing JOZU_USERNAME or JOZU_PASSWORD in " +
                         "environment variables. Both are required. " +
                         "Please set these variables in your .env " +
                         "file and try again.")
    return {
        "username": username,
        "password": password,
        "registry": os.getenv("JOZU_REGISTRY"),
        "namespace": os.getenv("JOZU_NAMESPACE")
    }



