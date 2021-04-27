"""git相关的动作."""
import os
import warnings
import configparser
import time
from pathlib import Path
from typing import Optional, Callable, Dict, List
from git import Repo
from git.repo.fun import is_git_dir
import git
from pmfp.utils.run_command_utils import run, make_env_args


def make_repod(p: Path) -> Path:
    d = p.joinpath(".git")
    return d


def git_find_remotes(p: Path) -> Dict[str, str]:
    """从git项目中找到远端仓库url.

    Args:
        p (Path): 目标地址

    Raises:
        AttributeError: 如果路径不是git项目则会抛出

    Returns:
        Dict[str, str]: 远程仓库的本地命名和对应地址

    """
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            result = {}
            for i in repo.remotes:
                urls = list(i.urls)
                if urls:
                    result[i.name] = urls[0]
            return result


def git_find_origin(p: Path) -> Optional[str]:
    """从git项目中找到远端origin仓库url.

    Args:
        p (Path): 目标地址

    Raises:
        AttributeError: 如果路径不是git项目则会抛出

    Returns:
        Optional[str]: 远程origin仓库的对应地址

    """
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            for i in repo.remotes:
                if i.name == "origin":
                    urls = list(i.urls)
                    if urls:
                        return urls[0]
                    raise AttributeError(f"origin未设置路径")
            else:
                return None


def git_add_remote(p: Path, remote_name: str, remote_url: str) -> None:
    """为本地git仓库关联远程仓库.

    Args:
        p (Path): 本地仓库路径
        remote_name (str): 远程仓库名
        remote_url (str): 远程仓库url

    Raises:
        AttributeError: 如果路径不是git项目则会抛出

    """
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            for i in repo.remotes:
                if remote_name == i.name:
                    raise AttributeError(f"远程仓库名{remote_name}已被设置")
            repo.create_remote(remote_name, remote_url)


def git_add_origin(p: Path, remote_url: str) -> None:
    """为本地git仓库关联origin远程仓库

    Args:
        p (Path): 本地仓库路径
        remote_url (str): 远程仓库url

    Raises:
        AttributeError: 如果路径不是git项目则会抛出

    """
    git_add_remote(p, remote_name="origin", remote_url=remote_url)


def git_init(p: Path, *, remote_url: Optional[str] = None) -> None:
    """初始化本地git仓库.

    Args:
        p ( Path ): 本地git仓库位置
        remote_url (Optional[str], optional): 远程关联仓库url. Defaults to None.

    """
    with Repo.init(p, mkdir=True) as repo:
        print("git本地仓库初始化完成.")
        if remote_url:
            repo.create_remote('origin', remote_url)
            print("绑定远程仓库完成")


def git_clone(url: str, to: Path, *,
              branch: str = "master") -> None:
    """从远程克隆项目到本地.

    Args:
        url (str): 远程url
        to (Path): 本地项目路径
        branch (str, optional): 拉取的分支. Defaults to "master".
    """
    # with Repo.clone_from(url, to_path=to, multi_options=[f"--branch={branch}"], config='http.sslVerify=false'):
    #     print("git clone ok")
    run(f'git clone -b {branch} -c http.sslVerify=false {url} {to}', visible=True)
    print("git clone ok")


def get_latest_commits(p: Path) -> Dict[str, str]:
    """获取git项目的各个分支最近一次commit的hash值.

    Args:
        p (Path): [description]

    Raises:
        AttributeError: 如果路径不是git项目则会抛出

    Returns:
        Dict[str, str]: [description]
    """

    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            result = {}
            for i in repo.heads:
                result[i.name] = i.commit.hexsha
            return result


def get_master_latest_commit(p: Path) -> str:
    """获取git项目的最近一个master分支的commit号.

    Args:
        p (Path): git项目位置

    Raises:
        AttributeError: 如果路径不是git项目则会抛出
        AttributeError: git仓库没有master或者main分支

    Returns:
        str: commit号

    """
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        infos = run("git show-ref master", cwd=p)
        for line in infos.splitlines():
            hs, ref = line.split(" ")
            if ref == "refs/heads/master" or ref == "refs/heads/main":
                return hs
        else:
            raise AttributeError("git仓库没有master或者main分支")
        # with Repo(d) as repo:
        #     for i in repo.heads:
        #         if i.name == "master" or i.name == "main":
        #             return i.commit.hexsha
        #     else:
        #         raise AttributeError("git仓库没有master或者main分支")


def git_push(p: Path, *, msg: str = "update") -> None:
    """git项目推代码到远端仓库.

    Args:
        p (Path): 本地仓库位置
        msg (str): 注释消息

    """
    d = make_repod(p)
    with Repo(d) as repo:
        repo.index.add(".")
        print("git add .执行成功")
        now = time.time()
        repo.index.commit(message=f"{msg} commit @{now}")
        print("git commit执行成功")
        repo.remote().pull()
        print("git pull执行成功")
        repo.remote().push()
        print("git push执行成功")


def git_pull_master(p: Path) -> None:
    """git项目推代码到远端仓库.

    Args:
        p (Path): 本地仓库位置
        msg (str): 注释消息

    """
    # print(f"pull path {p}********************")
    # d = make_repod(p)
    # with Repo() as repo:
    #     if str(repo.active_branch) != "master":
    #         warnings.warn(f"active_branch {repo.active_branch} not master")
    #         return
    run("git pull", cwd=p, env=make_env_args(["GIT_SSL_NO_VERIFY::1"]), visible=True, fail_exit=False)


def git_new_tag(p: Path, version: str, message: Optional[str] = None, remote: bool = False) -> None:
    """为代码打tag.

    Args:
        p (Path): 本地仓库位置
        version (str): 项目代码版本
        message (Optional[str]): tag的消息
        remote (bool): 是否推送到远程仓库origin

    """
    d = make_repod(p)
    tag = f"v{version}"
    if version.startswith("v"):
        tag = version
    with Repo(d) as repo:
        repo.create_tag(tag, message=message)
        print("git new tag 执行成功")
        if remote is True:
            repo.remote().push(tags=True)
            print(f"tag {tag} 推送至远程仓库")
