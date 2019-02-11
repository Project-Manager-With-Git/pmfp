"""执行项目的默认执行项."""
import subprocess
from typing import Dict, Any, Optional
from pmfp.utils import get_python_path


def run(config: Dict[str, Any], cmd: Optional[str])->None:
    """执行项目的默认执行项.

    Args:
        config (Dict[str, Any]): 项目的配置字典
        cmd (Optional[str]): 执行的额外命令字符串
    """
    if config["project-language"] == "Python":
        entry = config["entry"]
        if not entry:
            print("请先在配置文件中指定入口")
            return
        python = get_python_path(config)
        if cmd:
            command = f"{python} {entry} {cmd}"
        else:
            command = f"{python} {entry}"
        subprocess.check_call(command, shell=True)
    elif config["project-language"] == "Javascript":
        if cmd:
            command = f"npm start {cmd}"
        else:
            command = f"npm start"
        subprocess.check_call(command, shell=True)
