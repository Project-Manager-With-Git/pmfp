"""构造不同执行环境."""
from typing import Dict, Any, List
from pmfp.utils.run_command_utils import run_command,get_global_python


def new_env(env:str,*,
        root:str,
        project_name:str,
        project_version:str,
        project_license:str,
        author:str,
        author_email:str,
        keywords:List[str],
        description:str) -> None:
    """构造不同执行环境.

    Args:
        port (str): 端口
        root (str): 启动的根目录
        bind (str): 绑定的ip
    """
    if env == "py":
        
    run_command(command)