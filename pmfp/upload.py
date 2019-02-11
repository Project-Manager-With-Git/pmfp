"""上传项目到git仓库."""
import time
import subprocess
import configparser
from typing import Dict, Any
from pmfp.const import PROJECT_HOME


def _git_check()->bool:
    """检测项目有没有.git可以用于上传和打标签等操作."""
    if not PROJECT_HOME.joinpath(".git").exists():
        return False
    else:
        return True


def _git_check_and_find_remote()->str:
    """从项目的.git中找到远端仓库url."""
    if not _git_check():
        raise AttributeError("upload to git should have a .git dir in root path")
    else:
        pointgit = PROJECT_HOME.joinpath(".git")
        gitconfig = pointgit.joinpath('config')
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(str(gitconfig))
        path = parser['remote "origin"']['url']
        return path


def git_tag(config: Dict[str, Any])->None:
    """为项目打标签.

    Args:
        config (Dict[str, Any]): 项目的配置字典
    """
    remote = _git_check_and_find_remote()
    version = config["version"]
    status = config["status"]
    tag = "{status}-{version}".format(version=version, status=status)
    command = f"git tag -a {tag} -m 'version: {tag}'"
    subprocess.check_call(command, shell=True)
    command = f"git push --tag"
    subprocess.check_call(command, shell=True)
    print(f"push tag {tag} for package to {remote} done")


def git_push(msg: str = None)->None:
    """对项目推代码.

    Args:
            config (Dict[str, Any]): 项目的配置字典
            msg (str, optional): Defaults to None. 顺便的要添加的提交信息

    Returns:
            None: [description]

    """
    remote = _git_check_and_find_remote()

    command = "git add ."
    subprocess.check_call(command, shell=True)
    command = f'git commit -m "{msg}@{time}"'
    subprocess.check_call(command, shell=True)

    command = "git pull"
    subprocess.check_call(command, shell=True)
    command = "git push"
    subprocess.check_call(command, shell=True)
    print(f"push code to {remote} done")


def upload(config: Dict[str, Any], kwargs: Dict[str, Any])->None:
    """将代码上传至远端git仓库.
    
    Args:
        config (Dict[str, Any]): 项目的配置字典
        kwargs (Dict[str, Any]): 上传的关键字参数.
    """
    msg = kwargs.get("msg")
    tag = kwargs.get("tag")
    git_push(msg)
    if tag:
        git_tag(config)
