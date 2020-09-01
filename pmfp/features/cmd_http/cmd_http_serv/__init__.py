"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any,List
from pmfp.utils.run_command_utils import run_command



def http_serv(port:str,root:str,bind:str)->None:
    bind_str = ""
    if bind:
        bind_str+= f"--bind {bind}"
    root_str = ""
    if root:
        root_str += f"--directory {root}" 
    command = f"python -m http.server {port} {bind_str} {root_str}"
    print(f"启动命令:{command}")
    run_command(command)