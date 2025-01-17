import json
import subprocess
import yaml
from typing import Any, Dict, List, Optional
from ..modelkit.utils import Color, IS_A_TTY
from .utils import _process_command_flags


def info(repo_path_with_tag: str, 
         filters: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
    """
    Retrieve information about a ModelKit, displaying the contents in the console,
    while returning the contents as a string-keyed dictionary.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag.
        filters (Optional[List[str]]): A list of kitfile parts for which to
            retrieve information. Defaults to None.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        The output of the 'kit info' command as a dictionary.       
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    
    Examples:
        >>> kit_info = info("jozu.ml/brett/titanic-survivability:latest")
        # Returns information from the local registry about the 
        # "titanic-survivability:latest" ModelKit.
        >>> print(kit_info["manifestVersion"])
        1.0
    """
    command = ["kit", "info",  
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)
 
    command.extend(_process_command_flags(kit_cmd_name="info", **kwargs))
    result = _run(command=command)
    kit_info = result.stdout.strip()
    print(kit_info)
    kit_info = yaml.safe_load(result.stdout.strip())
    return kit_info

def inspect(repo_path_with_tag: str, remote: Optional[bool] = True, **kwargs) -> Dict[str, Any]:
    """
    Inspect a ModelKit, displaying the contents in the console, while returning
    the contents as a string-keyed dictionary.

    Parameters:
    repo_path_with_tag (str): The path to the repository along with the tag.
    remote (Optional[bool]): Flag to indicate if the inspection should be done remotely. Defaults to True.
        Otherwise, the inspection will be done locally.
    **kwargs: Additional arguments to pass to the command.

    Returns:
        The output of the 'kit inspect' command as a dictionary.
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "inspect", 
                repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="inspect", **kwargs))
    result = _run(command=command)
    kit_inspect = result.stdout.strip()
    print(kit_inspect)
    kit_inspect = json.loads(result.stdout.strip())
    return(kit_inspect)

def list(repo_path_without_tag: Optional[str] = None, **kwargs) -> str:
    """
    Lists the ModelKits available in the specified repository path to the console,
    and returns the values as a string.

    Args:
        repo_path_without_tag (Optional[str]): The path to the repository without the tag. 
                                               If not provided, lists kits from the local registry.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        The list of available ModelKits as a string.
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "list"]
    if repo_path_without_tag:
        command.append(repo_path_without_tag)

    command.extend(_process_command_flags(kit_cmd_name="list", **kwargs))
    result = _run(command=command)
    kit_list = result.stdout.strip()
    print(kit_list)
    return(kit_list)

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
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = [
        "kit", "login", registry,
        "--username", user,
        "--password-stdin"
    ]

    command.extend(_process_command_flags(kit_cmd_name="login", **kwargs))
    result = _run(command=command, input=passwd)
    print(result.stdout)

def logout(registry: Optional[str] = "jozu.ml", **kwargs) -> None:
    """
    Logs out from the specified registry.

    Args:
        registry (str, optional): The registry to log out from. Defaults to "jozu.ml".
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "logout", registry]

    command.extend(_process_command_flags(kit_cmd_name="logout", **kwargs))
    result = _run(command=command)
    print(result.stdout)

def pack(repo_path_with_tag: str, **kwargs)-> None:
    """
    Packs the current directory into a ModelKit package with a specified tag.

    Args:
        repo_path_with_tag (str): The repository path along with the tag to be used for the package.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "pack", ".", 
               "--tag", repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pack", **kwargs))
    result = _run(command=command)
    print(result.stdout)

def pull(repo_path_with_tag: str, **kwargs) -> None:
    """
    Pulls the specified ModelKit from the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to pull.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "pull", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pull", **kwargs))
    result = _run(command=command)
    print(result.stdout)

def push(repo_path_with_tag: str, **kwargs) -> None:
    """
    Pushes the specified ModelKit to the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to be pushed.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "push", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="push", **kwargs))
    result = _run(command=command)
    print(result.stdout)

def remove(repo_path_with_tag: str, **kwargs) -> None:
    """
    Remove a ModelKit from the registry.

    Args:
        repo_path_with_tag (str): The path to the repository with its tag.
        **kwargs: Additional arguments to pass to the command.

    Returns:
        None
    
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status,
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "remove",  
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="remove", **kwargs))
    result = _run(command=command)
    print(result.stdout)
 

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
        subprocess.CalledProcessError: If the command returns a non-zero exit status. 
        The exception contains the return code and the standard error output.

    Examples:
        >>> tag("jozu.ml/brett/titanic-survivability:latest", 
                "jozu.ml/brett/titanic-survivability:v2")
    """
    command = ["kit", "tag", 
               repo_path_with_tag, 
               repo_path_with_new_tag]

    command.extend(_process_command_flags(kit_cmd_name="tag", **kwargs))
    result = _run(command=command)
    print(result.stdout)

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
    
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status. 
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "unpack", 
               "--dir", dir, 
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)

    command.extend(_process_command_flags(kit_cmd_name="unpack", **kwargs))
    result = _run(command=command)
    print(result.stdout)

def version(**kwargs) -> str:
    """
    Displays the version of the KitOps Command-line Interface (CLI) to the console
    and returns the value as a string.

    Args:
        **kwargs: Additional arguments to pass to the command.

    Returns:
        The KitOps CLI version as a string.
    
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status. 
        The exception contains the return code and the standard error output.
    """
    command = ["kit", "version"]

    command.extend(_process_command_flags(kit_cmd_name="version", **kwargs))
    result = _run(command=command)
    version = result.stdout.strip()
    print(version)
    return version

def _run(command: List[Any], input: Optional[str] = None, 
         verbose: bool = True, **kwargs) -> subprocess.CompletedProcess:
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
        The exception contains the return code and the standard error output.
    """
    if verbose:
        output = '% ' + ' '.join(command)
        if IS_A_TTY:
            output = f"{Color.CYAN.value}{output}{Color.RESET.value}"
        print(output, flush=True)

    # Because check=True is used, any non-zero exit status will raise a CalledProcessError.
    return subprocess.run(
        command, input=input, text=True, check=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )