"""执行命令行任务的通用组件."""
import subprocess
import chardet
from typing import Callable,Optional,Union,Mapping,Any
from termcolor import colored

def run_command(command:str,*,cwd:Optional[Any]=None,env:Optional[Any]=None,succ_cb:Optional[Callable[[],None]]=None,fail_cb:Optional[Callable[[],None]]=None)->None:
    """执行命令行命令.

    Args:
        command (str): 命令行命令
        succ_cb (Optional[Callable[[],None]], optional): 执行成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[],None]], optional): 执行失败的回调函数. Defaults to None.

    """
    res = subprocess.run(command, capture_output=True, shell=True,cwd=cwd,env=env)
    if res.returncode != 0:
        print(f"命令{command}执行失败")
        if res.stderr:
            encoding = chardet.detect(res.stderr).get("encoding")
            print(colored(res.stderr.decode(encoding).strip(),'white', 'on_magenta'))
        else:
            encoding = chardet.detect(res.stdout).get("encoding")
            print(colored(res.stdout.decode(encoding).strip(),'white', 'on_magenta'))
        if fail_cb:
            fail_cb()
    else:
        encoding = chardet.detect(res.stdout).get("encoding")
        print(colored(res.stdout.decode(encoding).strip(),'white', 'on_cyan'))
        if succ_cb:
            succ_cb()