"""执行项目的默认执行项."""
import subprocess
from typing import Dict, Any, Optional
from pmfp.utils import get_python_path

def run(config: Dict[str, Any], entry: Optional[str] = None, cmd: Optional[str] = None) -> None:
    """执行项目的默认执行项.

    Args:
        config (Dict[str, Any]): 项目的配置字典
        cmd (Optional[str]): 执行的额外命令字符串
    """
    l = config["project-language"]
    run_entry = None
    if entry:
        run_entry = entry
    else:
        entry = config["entry"]
        if entry:
            run_entry = entry
    if l == "Python":
        if not run_entry:
            print("请先在配置文件中指定入口,或者在参数中指定入口")
            return
        python = get_python_path(config)
        if cmd:
            command = f"{python} {run_entry} {cmd}"
        else:
            command = f"{python} {run_entry}"
        subprocess.check_call(command, shell=True)
    elif l == "Javascript":
        if not run_entry or run_entry == "es/index.js":
            if cmd:
                command = f"npm start {cmd}"
            else:
                command = f"npm start"
        else:
            env = config["env"]
            if env in ("node"):
                if cmd:
                    command = f"./node_modules/.bin/babel-node {run_entry} {cmd}"
                else:
                    command = f"./node_modules/.bin/babel-node {run_entry}"
            else:
                if cmd:
                    command = f"node {run_entry} {cmd}"
                else:
                    command = f"node {run_entry}"
        subprocess.check_call(command, shell=True)
    elif l == "Golang":
        if not run_entry:
            print("请先在配置文件中指定入口文件,或者在run命令中指定")
            return
        command = f"go run {run_entry}"
        subprocess.check_call(command, shell=True)
    else:
        print(f"目前run命令不支持{l}语言")
