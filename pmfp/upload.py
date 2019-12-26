"""上传项目到git仓库."""
import time
import subprocess
import configparser
import chardet
from typing import Dict, Any
from pmfp.const import PROJECT_HOME


def _git_check() -> bool:
    """检测项目有没有.git可以用于上传和打标签等操作."""
    if not PROJECT_HOME.joinpath(".git").exists():
        return False
    else:
        return True


def _git_check_and_find_remote() -> str:
    """从项目的.git中找到远端仓库url."""
    if not _git_check():
        raise AttributeError(
            "upload to git should have a .git dir in root path")
    else:
        pointgit = PROJECT_HOME.joinpath(".git")
        gitconfig = pointgit.joinpath('config')
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(str(gitconfig))
        path = parser['remote "origin"']['url']
        return path


def git_tag(config: Dict[str, Any]) -> None:
    """为项目打标签.

    Args:
        config (Dict[str, Any]): 项目的配置字典
    """
    remote = _git_check_and_find_remote()
    version = config["version"]
    status = config["status"]
    if config["project-language"] != "Golang":
        tag = f"{status}-{version}"
    else:
        tag = f"v{version}"
    command = f"git tag -a {tag} -m 'version: {tag}'"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("git tag 执行出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print("git tag 执行成功")
        encoding = chardet.detect(res.stdout).get("encoding")
        print(res.stdout.decode(encoding))
        command = f"git push --tag"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print("git push --tag执行出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print("git push --tag执行成功")
            encoding = chardet.detect(res.stdout).get("encoding")
            print(res.stdout.decode(encoding))
            print(f"推送 tag版本{tag}到git仓库{remote}完成")


def git_push(msg: str = None) -> None:
    """对项目推代码.

    Args:
            config (Dict[str, Any]): 项目的配置字典
            msg (str, optional): Defaults to None. 顺便的要添加的提交信息

    Returns:
            None: [description]

    """
    remote = _git_check_and_find_remote()

    command = "git add ."
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("git add .执行出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print("git add .执行成功")
        encoding = chardet.detect(res.stdout).get("encoding")
        print(res.stdout.decode(encoding))
        msg = msg or "push"
        now = time.time()
        command = f'git commit -m "{msg}@{now}"'
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print("git commit执行出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print("git commit执行成功")
            encoding = chardet.detect(res.stdout).get("encoding")
            print(res.stdout.decode(encoding))
            command = "git pull"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("git pull执行出错")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("git pull执行成功")
                encoding = chardet.detect(res.stdout).get("encoding")
                print(res.stdout.decode(encoding))
                command = "git push"
                res = subprocess.run(command, capture_output=True, shell=True)
                if res.returncode != 0:
                    print("git push执行出错")
                    encoding = chardet.detect(res.stderr).get("encoding")
                    print(res.stderr.decode(encoding))
                else:
                    print("git push执行成功")
                    encoding = chardet.detect(res.stdout).get("encoding")
                    print(res.stdout.decode(encoding))
                    print(f"推送源码到git仓库{remote}完成")


def upload(config: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
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
