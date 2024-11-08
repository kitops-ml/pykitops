import subprocess
from typing import Any, List, Optional
from ..modelkit.utils import Color, IS_A_TTY

def info(repo_path_with_tag: str, remote: Optional[bool] = True):
    """
    Retrieve information about a kit repository.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag.
        remote (Optional[bool]): If True, include the remote flag in the command. Defaults to True.

    Returns:
        None
    """
    remote_flag = "--remote" if remote else None
    command = ["kit", "info",  
               repo_path_with_tag]
    if remote_flag:
        command.append(remote_flag)
    _run(command=command)

def inspect(repo_path_with_tag: str, remote: Optional[bool] = True):
    """
    Inspect a repository using the 'kit' command.

    Parameters:
    repo_path_with_tag (str): The path to the repository along with the tag.
    remote (Optional[bool]): Flag to indicate if the inspection should be done remotely. Defaults to True.
        Otherwise, the inspection will be done locally.

    Returns:
        None
    """
    remote_flag = "--remote" if remote else None
    command = ["kit", "inspect", 
                repo_path_with_tag]
    if remote_flag:
        command.append(remote_flag)
    _run(command=command)

def list(repo_path_without_tag: Optional[str] = None):
    """
    Lists the ModelKits available in the specified repository path.

    Args:
        repo_path_without_tag (Optional[str]): The path to the repository without the tag. 
                                               If not provided, lists kits from the local registry.

    Returns:
        None
    """
    command = ["kit", "list"]
    if repo_path_without_tag:
        command.append(repo_path_without_tag)
    _run(command=command)

def login(user: str, passwd: str, registry: str = "jozu.ml"):
    """
    Logs in to the specified registry using the provided username and password.

    Args:
        user (str): The username for the registry.
        passwd (str): The password for the registry.
        registry (str, optional): The registry URL. Defaults to "jozu.ml".

    Returns:
        None
    """
    command = [
        "kit", "login", registry,
        "--username", user,
        "--password-stdin"
    ]
    _run(command=command, input=passwd)

def logout(registry: str = "jozu.ml"):
    """
    Logs out from the specified registry.

    Args:
        registry (str, optional): The registry to log out from. Defaults to "jozu.ml".

    Returns:
        None
    """
    command = ["kit", "logout", registry]
    _run(command=command)

def pack(repo_path_with_tag: str):
    """
    Packs the current directory into a ModelKit package with a specified tag.

    Args:
        repo_path_with_tag (str): The repository path along with the tag to be used for the package.

    Returns:
        None
    """
    command = ["kit", "pack", ".", 
               "--tag", repo_path_with_tag]
    _run(command=command)

def pull(repo_path_with_tag: str):
    """
    Pulls the specified ModelKit from the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to pull.

    Returns:
        None
    """
    command = ["kit", "pull", 
               repo_path_with_tag]
    _run(command=command)

def push(repo_path_with_tag: str):
    """
    Pushes the specified ModelKit to the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to be pushed.

    Returns:
        None
    """
    command = ["kit", "push", 
               repo_path_with_tag]
    _run(command=command)

def remove(repo_path_with_tag: str, remote: Optional[bool] = True):
    """
    Remove a ModelKit from the registry.

    Args:
        repo_path_with_tag (str): The path to the repository with its tag.
        remote (Optional[bool]): If True, the repository will be removed from the remote registry. Defaults to True.
            Otherwise, the repository will be removed from the local registry.

    Returns:
        None
    """
    remote_flag = "--remote" if remote else None
    command = ["kit", "remove",  
               repo_path_with_tag]
    if remote_flag:
        command.append(remote_flag)
    try:
        _run(command=command)
    except subprocess.CalledProcessError as e:
        # If the repository is not found in the registry, ignore the error
        pass

def unpack(repo_path_with_tag: str, dir: str):
    """
    Unpacks a ModelKit to the specified directory from the remote registry.

    This function constructs a command to unpack a ModelKit and 
    calls an internal function to execute the command.

    Args:
        repo_path_with_tag (str): The path to the repository along with 
            the tag to be unpacked.
        dir (str): The directory to unpack the ModelKit to.

    Returns:
        None
    """
    command = ["kit", "unpack", 
               "--dir", dir, 
               "--overwrite", 
               repo_path_with_tag]
    _run(command=command)

def version():
    """
    Lists the version of the KitOps Command-line Interface (CLI).

    Args:
        None
    Returns:
        None
    """
    command = ["kit", "version"]
    _run(command=command)


def _run(command: List[Any], input: Optional[str] = None, verbose: bool = True):
    """
    Executes a command in the system shell.

    Args:
        command (List[Any]): The command to be executed as a list of strings.
        input (Optional[str]): Optional input to be passed to the command.
        verbose (bool): If True, print the command before executing. Defaults to True.

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