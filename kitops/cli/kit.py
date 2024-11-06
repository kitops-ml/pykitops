import subprocess
from typing import Any, List, Optional


def kit_info(repo_path_with_tag, remote: Optional[bool] = True):
    remote_flag = "--remote" if remote else ""
    command = ["kit", "info", remote_flag,repo_path_with_tag]
    _run(command=command)

def kit_inspect(repo_path_with_tag, remote: Optional[bool] = True):
    remote_flag = "--remote" if remote else ""
    command = ["kit", "inspect", remote_flag, repo_path_with_tag]
    _run(command=command)

def kit_list(repo_path_without_tag: Optional[str] = None):
    command = ["kit", "list", repo_path_without_tag]
    _run(command=command)

def kit_login(user: str, passwd: str, registry: str = "jozu.ml"):
    command = ["kit", "login", registry, "--username", user, "--password-stdin"]
    _run(command=command, input=passwd)

def kit_logout(registry: str = "jozu.ml"):
    command = ["kit", "logout", registry]
    _run(command=command)

def kit_pack(repo_path_with_tag: str):
    command = ["kit", "pack", ".", "--tag", repo_path_with_tag]
    _run(command=command)

def kit_pull(repo_path_with_tag):
    command = ["kit", "pull", repo_path_with_tag]
    _run(command=command)

def kit_push(repo_path_with_tag):
    command = ["kit", "push", repo_path_with_tag]
    _run(command=command)

def kit_remove(repo_path_with_tag, remote: Optional[bool] = True):
    remote_flag = "--remote" if remote else ""
    command = ["kit", "remove", remote_flag, repo_path_with_tag]
    _run(command=command)

def kit_unpack(repo_path_with_tag):
    command = ["kit", "unpack", "--overwrite", repo_path_with_tag]
    _run(command=command)

def _run(command: List[Any], input: Optional[str] =None):
    print(' '.join(command), flush=True)
    subprocess.run(command, input=input, text=True)