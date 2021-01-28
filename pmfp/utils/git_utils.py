"""git相关的动作."""
import configparser
import time
from pathlib import Path
from typing import Optional, Callable, Dict, List
from git import Repo
from git.repo.fun import is_git_dir
from pmfp.const import PLATFORM


def make_repod(p: Path) -> Path:
    if PLATFORM == "windows":
        d = p.joinpath(".git")
    else:
        d = p
    return d


# class NoRemoteURL(Exception):
#     """目标项目没有指定远程仓库."""


def git_find_remotes(p: Path) -> Dict[str, str]:
    """从项目的.git中找到远端仓库url.

    Args:
        p (Path): 目标地址

    Raises:
        AttributeError: 如果路径下没有`.git`文件夹则会报错.

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


def git_find_origin(p: Path) -> str:
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            result = {}
            for i in repo.remotes:
                if i.name == "origin":
                    urls = list(i.urls)
                    if urls:
                        return urls[0]
                    raise AttributeError(f"origin未设置路径")


def git_add_remote(p: Path, remote_name: str, remote_url: str) -> None:
    """为本地git仓库关联远程仓库.

    Args:
        p (Path): 本地仓库路径
        remote_name (str): 远程仓库名
        remote_url (str): 远程仓库url

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
    with Repo.clone_from(url, to_path=to, multi_options=[f"--branch={branch}"]) as repo:
        print("git clone ok")


def get_latest_commits(p: Path) -> Dict[str, str]:
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

    Returns:
        str: commit号

    """
    d = make_repod(p)
    if not is_git_dir(d):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        with Repo(d) as repo:
            for i in repo.heads:
                if i.name == "master":
                    return i.commit.hexsha
            else:
                raise AttributeError(f"git仓库没有master分支")


def git_push(p: Path, msg: str = "update") -> None:
    """git项目推代码到远端仓库.

    Args:
        p (Path): 本地仓库位置
        msg (str): 注释消息

    """
    remote = _git_find_remote(p)
    command = "git add ."

    def git_add_succeed_callback(_: str) -> None:
        print("git add .执行成功")

        def git_commit_succeed_callback(_: str) -> None:
            print("git commit执行成功")

            def git_pull_succeed_callback(_: str) -> None:
                print("git pull执行成功")
                command = "git push"
                run_command(command,
                            cwd=p,
                            succ_cb=lambda x: print(f"推送源码到git仓库 {remote} 成功")
                            )

            command = "git pull"
            run_command(command,
                        cwd=p,
                        succ_cb=git_pull_succeed_callback
                        )

        now = time.time()
        command = f'git commit -m "{msg}@{now}"'
        run_command(command,
                    cwd=p,
                    succ_cb=git_commit_succeed_callback
                    )

    run_command(command,
                cwd=p,
                succ_cb=git_add_succeed_callback
                )


def git_tag(p: Path, version: str) -> None:
    """为代码打tag.

    Args:
        p (Path): 本地仓库位置
        version (str): 项目代码版本

    """
    remote = _git_find_remote(p)
    tag = f"v{version}"

    def git_tag_succeed_callback(_: str) -> None:
        print(f"git tag -a {tag} -m 'version: {tag}' 执行成功")
        command = "git push --tag"
        run_command(command,
                    cwd=p,
                    succ_cb=lambda x: print(f"推送 tag版本{tag}到git仓库{remote}完成")
                    )

    command = f"git tag -a {tag} -m 'version: {tag}'"
    run_command(command,
                cwd=p,
                succ_cb=git_tag_succeed_callback
                )
