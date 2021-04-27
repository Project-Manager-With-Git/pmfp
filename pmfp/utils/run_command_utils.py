"""执行命令行任务的通用组件."""
import sys
import os
import warnings
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
import chardet
from termcolor import colored


def make_env_args(env_args: Optional[List[str]]) -> Dict[str, str]:
    """构造环境变量字典

    Args:
        env_args (Optional[List[str]]): 外部添加环境变量字符串,以`::`区分键值

    Returns:
        Dict[str, str]: 执行时的环境变量字典
    """
    default_environ = dict(os.environ)
    env = {}
    env.update(default_environ)
    if env_args:
        for i in env_args:
            try:
                key, value = i.split("::")
            except:
                warnings.warn(f"{i} not support as env_args,skip")
                continue
            else:
                env[key] = value
    return env


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
        if command.startswith("[") and command.endswith("]"):
            try:
                command_list = eval(command)
            except SyntaxError:
                print(colored(f"""命令:{command} 语法错误""", 'white', 'on_red'))
                sys.exit(1)
            except Exception:
                print(colored(f"""命令:{command} 解析错误""", 'white', 'on_red'))
                sys.exit(1)
            else:
                res = subprocess.run(command_list, capture_output=True, shell=True, check=True, cwd=cwd, env=env)
        else:
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
