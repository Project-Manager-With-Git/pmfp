"""执行命令行任务的通用组件."""
import subprocess
import warnings
from pathlib import Path
from typing import Callable, Optional, Any
import chardet
from termcolor import colored
from pmfp.const import GOLBAL_PYTHON


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



def get_node_version() -> Optional[str]:
    """获取系统中node的版本."""
    command = "node -v"
    result = None
    def node_succ_cb(content:str)->None:
        result = content[1:]

    def node_fail_cb(_:str)->None:
        warnings.warn("系统中未找到node环境,如有需要请安装")
    run_command(command,succ_cb=node_succ_cb,fail_cb=node_fail_cb)
    return result
        


def get_golang_version() -> Optional[str]:
    """获取本地golang的版本."""
    command = "go version"
    result = None
    def go_succ_cb(content:str)->None:
        result = [i for i in content.split(" ") if "."in i][0][2:]

    def go_fail_cb(_:str)->None:
        warnings.warn("系统中未找到golang环境,如有需要请安装")
    run_command(command,succ_cb=go_succ_cb,fail_cb=go_fail_cb)
    return result


def get_protoc_version() -> Optional[str]:
    """获取本地protoc的版本."""
    command = "protoc --version"
    result = None
    def go_succ_cb(content:str)->None:
        result = [i for i in content.split(" ") if "."in i][0]

    def go_fail_cb(_:str)->None:
        warnings.warn("系统中未找到protoc环境,如有需要请安装")
    run_command(command,succ_cb=go_succ_cb,fail_cb=go_fail_cb)
    return result


def get_local_python_path(env_path_str:str) -> str:
    """获取本地环境python解释器的地址.

    Args:
        env_path_str (str): python本地环境目录.

    Returns:
        str: python位置字符串

    """
    env_path = Path(env_path_str)
    python_path = env_path.joinpath("bin/python")
    if not python_path.exists():
        python_path = env_path.joinpath("Scripts/python")
        if not python_path.exists():
            python_path = env_path.joinpath("python")
            if not python_path.exists():
                warnings.warn("目录中未找到python环境.使用全局python")
                return GOLBAL_PYTHON
    return str(python_path)