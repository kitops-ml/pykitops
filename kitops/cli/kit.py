import subprocess
from typing import Any, List, Optional
from ..modelkit.utils import Color, IS_A_TTY
from .utils import _process_command_flags


def info(repo_path_with_tag: str, 
         filters: Optional[List[str]] = None, **kwargs) -> None:
    """
    Retrieve information about a kit repository.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag.
        filters (Optional[List[str]]): A list of kitfile parts for which to
            retrieve information. Defaults to None.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None

    
    Examples:
        >>> info("jozu.ml/brett/titanic-survivability:latest")
        # Returns information from the local registry about the 
        # "titanic-survivability:latest" ModelKit.
    """
    command = ["kit", "info",  
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)
 
    command.extend(_process_command_flags(kit_cmd_name="info", **kwargs))
    _run(command=command)

def inspect(repo_path_with_tag: str, remote: Optional[bool] = True, **kwargs) -> None:
    """
    Inspect a repository using the 'kit' command.

    Parameters:
    repo_path_with_tag (str): The path to the repository along with the tag.
    remote (Optional[bool]): Flag to indicate if the inspection should be done remotely. Defaults to True.
        Otherwise, the inspection will be done locally.
    **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "inspect", 
                repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="inspect", **kwargs))
    _run(command=command)

def list(repo_path_without_tag: Optional[str] = None, **kwargs) -> None:
    """
    Lists the ModelKits available in the specified repository path.

    Args:
        repo_path_without_tag (Optional[str]): The path to the repository without the tag. 
                                               If not provided, lists kits from the local registry.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "list"]
    if repo_path_without_tag:
        command.append(repo_path_without_tag)

    command.extend(_process_command_flags(kit_cmd_name="list", **kwargs))
    _run(command=command)

def login(user: str, passwd: str, registry: Optional[str] = "jozu.ml", **kwargs) -> None:
    """
    Logs in to the specified registry using the provided username and password.

    Args:
        user (str): The username for the registry.
        passwd (str): The password for the registry.
        registry (str, optional): The registry URL. Defaults to "jozu.ml".
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = [
        "kit", "login", registry,
        "--username", user,
        "--password-stdin"
    ]

    command.extend(_process_command_flags(kit_cmd_name="login", **kwargs))
    _run(command=command, input=passwd)

def logout(registry: Optional[str] = "jozu.ml", **kwargs) -> None:
    """
    Logs out from the specified registry.

    Args:
        registry (str, optional): The registry to log out from. Defaults to "jozu.ml".
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "logout", registry]

    command.extend(_process_command_flags(kit_cmd_name="logout", **kwargs))
    _run(command=command)

def pack(repo_path_with_tag: str, **kwargs)-> None:
    """
    Packs the current directory into a ModelKit package with a specified tag.

    Args:
        repo_path_with_tag (str): The repository path along with the tag to be used for the package.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "pack", ".", 
               "--tag", repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pack", **kwargs))
    _run(command=command)

def pull(repo_path_with_tag: str, **kwargs) -> None:
    """
    Pulls the specified ModelKit from the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to pull.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "pull", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pull", **kwargs))
    _run(command=command)

def push(repo_path_with_tag: str, **kwargs) -> None:
    """
    Pushes the specified ModelKit to the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to be pushed.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "push", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="push", **kwargs))
    _run(command=command)

def remove(repo_path_with_tag: str, **kwargs) -> None:
    """
    Remove a ModelKit from the registry.

    Args:
        repo_path_with_tag (str): The path to the repository with its tag.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "remove",  
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="remove", **kwargs))

    try:
        _run(command=command)
    except subprocess.CalledProcessError as e:
        # If the repository is not found in the registry, ignore the error
        pass

def tag(repo_path_with_tag: str, repo_path_with_new_tag: str, **kwargs) -> None:
    """
    Tag a ModelKit with a new tag.

    Args:
        repo_path_with_tag (str): The path to the repository with its tag.
        repo_path_with_new_tag (str): The new tag to be assigned to the ModelKit.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status

    Examples:
        >>> tag("jozu.ml/brett/titanic-survivability:latest", 
                "jozu.ml/brett/titanic-survivability:v2")
    """
    command = ["kit", "tag", 
               repo_path_with_tag, 
               repo_path_with_new_tag]

    command.extend(_process_command_flags(kit_cmd_name="tag", **kwargs))
    _run(command=command)

def unpack(repo_path_with_tag: str, dir: str, 
           filters: Optional[List[str]] = None, **kwargs) -> None:
    """
    Unpacks a ModelKit to the specified directory from the remote registry.

    This function constructs a command to unpack a ModelKit and 
    calls an internal function to execute the command.

    Args:
        repo_path_with_tag (str): The path to the repository along with 
            the tag to be unpacked.
        dir (str): The directory to unpack the ModelKit to.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "unpack", 
               "--dir", dir, 
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)

    command.extend(_process_command_flags(kit_cmd_name="unpack", **kwargs))
    _run(command=command)

def version(**kwargs) -> None:
    """
    Lists the version of the KitOps Command-line Interface (CLI).

    Args:
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    """
    command = ["kit", "version"]

    command.extend(_process_command_flags(kit_cmd_name="version", **kwargs))
    _run(command=command)


def _run(command: List[Any], input: Optional[str] = None, 
         verbose: bool = True, **kwargs) -> None:
    """
    Executes a command in the system shell.

    Args:
        command (List[Any]): The command to be executed as a list of strings.
        input (Optional[str]): Optional input to be passed to the command.
        verbose (bool): If True, print the command before executing. Defaults to True.
        **kwargs: Additional arguments to pass to the command.
        
    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """
    if verbose:
        output = '% ' + ' '.join(command)
        if IS_A_TTY:
            output = f"{Color.CYAN.value}{output}{Color.RESET.value}"
        print(output, flush=True)

    subprocess.run(command, input=input, text=True, check=True)