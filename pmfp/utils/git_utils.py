"""git相关的动作."""
import configparser
import time
from pathlib import Path
from typing import Optional, Callable
from .run_command_utils import run_command


def _git_check(p: Path) -> bool:
    """检测项目有没有.git可以用于上传和打标签等操作.

    Args:
        p (Path): 目标地址

    Returns:
        bool: 是否是git项目

    """
    if not p.joinpath(".git").exists():
        return False
    else:
        return True


class NoRemoteURL(Exception):
    """目标项目没有指定远程仓库."""


def _git_find_remote(p: Path) -> str:
    """从项目的.git中找到远端仓库url.

    Args:
        p (Path): 目标地址

    Raises:
        AttributeError: 如果路径下没有`.git`文件夹则会报错.

    Returns:
        str: 远程仓库的地址

    """
    if not _git_check(p):
        raise AttributeError(f"目标路径{p}不是git仓库.")
    else:
        pointgit = p.joinpath(".git")
        gitconfig = pointgit.joinpath('config')
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(str(gitconfig))
        url = parser['remote "origin"']['url']
        if url:
            return url
        else:
            raise NoRemoteURL(f"目标路径{p}的git仓库未指定远程仓库.")


def git_add_remote(p: Path, remote_url: str) -> None:
    """为本地git仓库关联远程仓库.

    Args:
        p (Path): 本地仓库路径
        remote_url (str): 远程仓库url

    """
    try:
        _ = _git_find_remote(p)
    except NoRemoteURL as e:

        def git_remoteadd_succeed_callback(_: str) -> None:
            command = "git fetch --all"
            run_command(command,
                        cwd=p,
                        succ_cb=lambda x: print(f"添加远程仓库{remote_url}到本地仓库{p}.")
                        )

        command = f"git remote add origin {remote_url}"
        run_command(command,
                    cwd=p,
                    succ_cb=git_remoteadd_succeed_callback)
    except Exception as e:
        raise e
    else:
        print(f"本地git项目{p}已经有了远程仓库")


def git_init(p: Path, *, remote_url: Optional[str] = None) -> None:
    """初始化本地git仓库.

    Args:
        p ( Path ): 本地git仓库位置
        remote_url (Optional[str], optional): 远程关联仓库url. Defaults to None.

    """
    def git_init_succeed_cb(x: str) -> None:
        print("git本地仓库初始化完成.")
        if remote_url:
            git_add_remote(p, remote_url)

    command = f"git init {str(p)}"
    run_command(command,
                succ_cb=git_init_succeed_cb)


def git_clone(url: str, to: Path, *,
              branch: str = "master", succ_cb: Optional[Callable[[str], None]] = None,
              fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """从远程克隆项目到本地.

    Args:
        url (str): 远程url
        to (Path): 本地项目路径
        branch (str, optional): 拉取的分支. Defaults to "master".
        succ_cb (Optional[Callable[[],None]], optional): 拉取成功的回调. Defaults to None.
        fail_cb (Optional[Callable[[],None]], optional): 拉取失败的回调. Defaults to None.

    """
    command = f"git clone -b {branch} {url} {str(to)}"
    run_command(command, succ_cb=succ_cb, fail_cb=fail_cb)


def get_latest_commit(p: Path) -> str:
    """获取git项目的最近一个master分支的commit号.

    Args:
        p (Path): git项目位置

    Returns:
        str: commit号

    """
    command = "git fetch --depth=1"
    result = ""

    def get_latest_succcb(_: str) -> None:
        nonlocal result
        with open(p.joinpath(".git/FETCH_HEAD"), "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "master" in line:
                    eles = line.split("\t")
                    result = eles[0]
                    break

    run_command(command, cwd=p, succ_cb=get_latest_succcb)
    return result


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
