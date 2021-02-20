"""执行命令行任务的通用组件."""
import sys
import subprocess
from functools import partial
from pathlib import Path
from typing import Callable, Optional, Any, Dict
import chardet
from termcolor import colored


def run(command: str, *, cwd: Optional[Path] = None, env: Optional[Dict[str, str]] = None, visible: bool = False, fail_exit: bool = False) -> str:
    """执行命令行命令并返回其stdout的值

    Args:
        command (str): 命令行命令
        cwd (Optional[Path]): 执行命令时的位置.Default: None
        env (Optional[Any]): 执行命令时的环境变量. Default:None
        visible (bool): 命令结果的可见度. Default: False
        fail_exit (bool): 当执行失败时退出程序. Default: False

    Returns:
        str: stdout捕获的字符串
    """
    try:
        if visible:
            print(colored(f"""执行命令:
            {command}""", 'white', 'on_blue'))
        res = subprocess.run(command, capture_output=True, shell=True, check=True, cwd=cwd, env=env)
    except subprocess.CalledProcessError as ce:
        print(colored(f"""命令:
        {command}
        执行失败""", 'white', 'on_red'))
        if ce.stderr:
            encoding = chardet.detect(ce.stderr).get("encoding")
            content = ce.stderr.decode(encoding).strip()
        else:
            encoding = chardet.detect(ce.stdout).get("encoding")
            content = ce.stdout.decode(encoding).strip()
        if visible:
            print(colored(content, 'white', 'on_magenta'))
        if fail_exit:
            sys.exit(1)
        else:
            raise ce
    except Exception as e:
        print(colored(f"""命令:
        {command}
        执行失败""", 'white', 'on_red'))
        if visible:
            print(f"error: {type(e)}")
            print(f"error_message: {str(e)}")
        if fail_exit:
            sys.exit(1)
        else:
            raise e
    else:

        content = ""
        if res.stdout:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()
        if visible:
            print(colored(f"""命令:
            {command}
            执行成功""", 'white', 'on_green'))
            print(colored(content, 'white', 'on_yellow'))
        return content
