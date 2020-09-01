"""执行命令行任务的通用组件."""
import subprocess
import chardet
from typing import Callable,Optional

def run_command(command:str,*,succ_cb:Optional[Callable[[],None]]=None,fail_cb:Optional[Callable[[],None]]=None)->None:
    """执行命令行命令.

    Args:
        command (str): 命令行命令
        succ_cb (Optional[Callable[[],None]], optional): 执行成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[],None]], optional): 执行失败的回调函数. Defaults to None.
    """
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"命令{command}执行失败")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
        if fail_cb:
            fail_cb()
    else:
        if succ_cb:
            succ_cb()