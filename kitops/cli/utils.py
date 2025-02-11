"""
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
"""

from typing import List, Optional


def _process_flag(
    full_key_name: str,
    abbr_key_name: Optional[str] = None,
    has_value_part: Optional[bool] = False,
    **kwargs,
) -> List[str]:
    """
    Processes the flag specified by key_full_name, it it exists

    Args:
        **kwargs: The arguments from which to extract the specified flag to be
        processed, if found.

    Returns:
        List[str]: The processed flag, if found; otherwise, an empty list.
    """
    flag = []
    found_full_key_name = kwargs.get(full_key_name, False)
    found_abbr_key_name = kwargs.get(abbr_key_name, False) if abbr_key_name else False
    if found_full_key_name:
        flag.append(f"--{full_key_name}")
        if has_value_part:
            value = kwargs.get(full_key_name, None)
            if value:
                flag.append(value)
    elif found_abbr_key_name:
        flag.append(f"-{abbr_key_name}")
        if has_value_part:
            value = found_abbr_key_name
            if value:
                flag.append(value)
    return flag


def _get_all_flag(**kwargs) -> List[str]:
    """
    Processes the all flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the all flag to be
        processed, if provided.

    Returns:
        List[str]: The processed all flag, if provided; otherwise, an empty list.
    """
    return _process_flag(full_key_name="all", abbr_key_name="a", **kwargs)


def _get_cert_flag(**kwargs) -> List[str]:
    """
    Processes the cert flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the cert flag to be
        processed, if provided.

    Returns:
        List[str]: The processed cert flag, if provided; otherwise, an empty list.
    """
    return _process_flag(full_key_name="cert", has_value_part=True, **kwargs)


def _get_compression_flag(**kwargs) -> List[str]:
    """
    Processes the compression flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the compression flag to be
        processed, if provided.

    Returns:
        List[str]: The processed compression flag, if provided; otherwise,
            an empty list.
    """
    return _process_flag(full_key_name="compression", has_value_part=True, **kwargs)


def _get_concurrency_flag(**kwargs) -> List[str]:
    """
    Processes the concurrency flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the concurrency flag to be
        processed, if provided.

    Returns:
        List[str]: The processed concurrency flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="concurrency", has_value_part=True, **kwargs)


def _get_dir_flag(**kwargs) -> List[str]:
    """
    Processes the dir flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the dir flag to be
        processed, if provided.

    Returns:
        List[str]: The processed dir flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(
        full_key_name="dir", abbr_key_name="d", has_value_part=True, **kwargs
    )


def _get_file_flag(**kwargs) -> List[str]:
    """
    Processes the file flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the file flag to be
        processed, if provided.

    Returns:
        List[str]: The processed file flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(
        full_key_name="file", abbr_key_name="f", has_value_part=True, **kwargs
    )


def _get_force_flag(**kwargs) -> List[str]:
    """
    Processes the force flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the force flag to be
        processed, if provided.

    Returns:
        List[str]: The processed force flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="force", abbr_key_name="f", **kwargs)


def _get_key_flag(**kwargs) -> List[str]:
    """
    Processes the key flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the key flag to be
        processed, if provided.

    Returns:
        List[str]: The processed key flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="key", has_value_part=True, **kwargs)


def _get_overwrite_flag(**kwargs) -> List[str]:
    """
    Processes the overwrite flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the overwrite flag
        to be processed, if provided.

    Returns:
        List[str]: The processed overwrite flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="overwrite", abbr_key_name="o", **kwargs)


def _get_plain_http_flag(**kwargs) -> List[str]:
    """
    Processes the plain-http flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the plain-http
        flag to be processed, if provided.

    Returns:
        List[str]: The processed plain-http flag, if provided; otherwise,
            an empty list.
    """
    return _process_flag(full_key_name="plain-http", **kwargs)


def _get_proxy_flag(**kwargs) -> List[str]:
    """
    Processes the proxy flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the proxy flag to be
        processed, if provided.

    Returns:
        List[str]: The processed proxy flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="proxy", has_value_part=True, **kwargs)


def _get_remote_flag(**kwargs) -> List[str]:
    """
    Processes the remote flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the remote flag to be
        processed, if provided.

    Returns:
        List[str]: The processed remote flag, if provided; otherwise,
        an empty list.
    """
    return _process_flag(full_key_name="remote", abbr_key_name="r", **kwargs)


def _get_show_update_notifications_flag(**kwargs) -> List[str]:
    """
    Processes the show-update-notifications flag for the KitOps CLI command,
    if provided.

    Args:
        **kwargs: The arguments from which to extract the show-update-notifications
        flag to be processed, if provided.

    Returns:
        List[str]: The processed show-update-notifications flag, if provided;
        otherwise,
            an empty list.
    """
    return _process_flag(full_key_name="show-update-notifications", **kwargs)


def _get_tag_flag(**kwargs) -> List[str]:
    """
    Processes the tag flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the tag flag to be
        processed, if provided.

    Returns:
        List[str]: The processed tag flag, if provided; otherwise, an empty list.
    """
    return _process_flag(
        full_key_name="tag", abbr_key_name="t", has_value_part=True, **kwargs
    )


def _get_tls_verify_flag(**kwargs) -> List[str]:
    """
    Processes the tls-verify flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the tls-verify
        flag to be processed, if provided.

    Returns:
        List[str]: The processed tls-verify flag, if provided; otherwise,
            an empty list.
    """
    return _process_flag(full_key_name="tls-verify", **kwargs)


def _get_token_flag(**kwargs) -> List[str]:
    """
    Processes the token flag for the KitOps CLI command, if provided.

    Args:
        **kwargs: The arguments from which to extract the token flag to be
        processed, if provided.

    Returns:
        List[str]: The processed token flag, if provided; otherwise, an empty list.
    """
    return _process_flag(full_key_name="token", has_value_part=True, **kwargs)


def _process_global_flags(**kwargs) -> List[str]:
    """
    Processes the global flags for the KitOps CLI.

    Args:
        **kwargs: The global flags to be processed.

    Returns:
        List[str]: The processed global flags.
    """
    flags = []
    for key, value in kwargs.items():
        if key in ["h", "v", "vv", "vvv"]:
            flags.append(f"-{key}")
        elif key in [
            "help",
            "verbose",
        ]:
            flags.append(f"--{key}")
        elif key in ["config", "log-level", "progress"]:
            if value is not None:
                flags.append(f"--{key}")
                flags.append(value)
    return flags


def _process_command_flags(kit_cmd_name: str, **kwargs) -> List[str]:
    """
    Processes the command-specific and global flags for the KitOps CLI.

    Args:
        **kwargs: The command-specific flags to be processed.

    Returns:
        List[str]: The processed command-specific flags.
    """
    flags = []
    if kit_cmd_name in [
        "info",
        "inspect",
        "list",
        "login",
        "pull",
        "push",
        "remove",
        "unpack",
    ]:
        flags.extend(_get_plain_http_flag(**kwargs))
        flags.extend(_get_tls_verify_flag(**kwargs))
        flags.extend(_get_cert_flag(**kwargs))
        flags.extend(_get_key_flag(**kwargs))
        flags.extend(_get_concurrency_flag(**kwargs))
        flags.extend(_get_proxy_flag(**kwargs))

    if kit_cmd_name in ["import"]:
        flags.extend(_get_tag_flag(**kwargs))
        flags.extend(_get_token_flag(**kwargs))

    if kit_cmd_name in ["init"]:
        flags.extend(_get_force_flag(**kwargs))

    if kit_cmd_name in ["pack"]:
        flags.extend(_get_file_flag(**kwargs))
        flags.extend(_get_compression_flag(**kwargs))

    if kit_cmd_name in ["remove"]:
        flags.extend(_get_all_flag(**kwargs))
        flags.extend(_get_force_flag(**kwargs))

    if kit_cmd_name in ["info", "inspect", "remove"]:
        flags.extend(_get_remote_flag(**kwargs))

    if kit_cmd_name in ["unpack"]:
        flags.extend(_get_overwrite_flag(**kwargs))

    if kit_cmd_name in ["version"]:
        flags.extend(_get_show_update_notifications_flag(**kwargs))

    flags.extend(_process_global_flags(**kwargs))

    return flags
