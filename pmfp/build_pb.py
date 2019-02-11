"""编译protobuf的schema为不同语言的代码."""

import subprocess
from typing import Dict, Any


def build_pb(config: Dict[str, Any], kwargs: Dict[str, Any])->None:
    """编译protobuf的schema为不同语言的代码.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        kwargs (Dict[str, Any]): 编译的配置信息字典.
    """
    name = kwargs.get("name")
    dir_ = kwargs.get("dir")
    default_lang = config["project-language"].lower() if (
        config["project-language"] != "Javascript"
    ) else "js"
    language = default_lang if not kwargs.get("language") else kwargs.get("language")
    grpc = kwargs.get("grpc")
    to = kwargs.get("to") if kwargs.get("to") else config["project-name"]
    if grpc:
        command = f"python -m grpc_tools.protoc -I{dir_} --{language}_out={to} \
            --grpc_{language}_out={to} {name}"
    else:
        command = f"protoc -I={dir_} --{language}_out={to} {dir_}/{name}"
    subprocess.check_call(command, shell=True)
