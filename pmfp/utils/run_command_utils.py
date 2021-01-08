"""执行命令行任务的通用组件."""
import subprocess
from functools import partial
from pathlib import Path
from typing import Callable, Optional, Any
import chardet
from termcolor import colored
from promise import Promise


def _run_command(resolve: Callable[[Any], Promise], reject: Callable[[Any], Promise],
                 command: str, *, cwd: Optional[Path] = None, env: Optional[Any] = None, visible: bool = False) -> Promise:
    res = subprocess.run(command, capture_output=True, shell=True, cwd=cwd, env=env)
    if res.returncode != 0:
        print(f"命令{command}执行失败")
        if res.stderr:
            encoding = chardet.detect(res.stderr).get("encoding")
            content = res.stderr.decode(encoding).strip()
        else:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()
        if visible:
            print(colored(content, 'white', 'on_magenta'))
        return reject(content)
    else:
        content = ""
        if res.stdout:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()

        if visible:
            print(colored(content, 'white', 'on_cyan'))
        return resolve(content)


def run_command(command: str, *, cwd: Optional[Path] = None, env: Optional[Any] = None, visible: bool = False) -> Promise:
    """执行命令行命令.

    Args:
        command (str): 命令行命令
        cwd (Optional[Path]): 执行命令时的位置.Default: None
        env (Optional[Any]): 执行命令时的环境变量. Default:None
        visible (bool): 命令结果的可见度. Default: False

    Return:
        (Promise): 可以在后续根据执行的成功与否添加回调
    """
    promise = Promise(
        partial(_run_command, command=command, cwd=cwd, env=env)
    )
    return promise
