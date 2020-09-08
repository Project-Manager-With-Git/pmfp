"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any, List
from pmfp.utils.run_command_utils import run_command,get_global_python


def http_serv(port: str, root: str, bind: str) -> None:
    """启动http静态服务.

    Args:
        port (str): 端口
        root (str): 启动的根目录
        bind (str): 绑定的ip
    """
    bind_str = ""
    if bind:
        bind_str += f"--bind {bind}"
    root_str = ""
    if root:
        root_str += f"--directory {root}"
    python = get_global_python()
    command = f"{GOLBAL_PYTHON} -m http.server {port} {bind_str} {root_str}"
    print(f"启动命令:{command}")
    run_command(command)
