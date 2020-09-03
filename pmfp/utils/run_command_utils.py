"""执行命令行任务的通用组件."""
import subprocess
from typing import Callable, Optional, Any
import chardet
from termcolor import colored


def default_succ_cb(content: str) -> None:
    """当执行成功时默认执行的回调."""
    print(colored(content, 'white', 'on_cyan'))


def default_fail_cb(content: str) -> None:
    """当执行失败时默认执行的回调."""
    print(colored(content, 'white', 'on_magenta'))


def run_command(command: str, *, cwd: Optional[Any] = None, env: Optional[Any] = None, succ_cb: Optional[Callable[[str], None]] = None, fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """执行命令行命令.

    Args:
        command (str): 命令行命令
        succ_cb (Optional[Callable[[str],None]], optional): 执行成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str],None]], optional): 执行失败的回调函数. Defaults to None.

    """
    res = subprocess.run(command, capture_output=True, shell=True, cwd=cwd, env=env)
    if res.returncode != 0:
        print(f"命令{command}执行失败")
        if res.stderr:
            encoding = chardet.detect(res.stderr).get("encoding")
            content = res.stderr.decode(encoding).strip()
        else:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()
        if fail_cb:
            fail_cb(content)
        else:
            default_fail_cb(content)
    else:
        content = ""
        if res.stdout:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()
        if succ_cb:
            succ_cb(content)
        else:
            default_succ_cb(content)
