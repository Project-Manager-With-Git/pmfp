"""编译protobuf的schema为不同语言的代码."""

import subprocess
from typing import Dict, Any
from pmfp.const import PROJECT_HOME


def build_pb(config: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
    """编译protobuf的schema为不同语言的代码.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        kwargs (Dict[str, Any]): 编译的配置信息字典.
    """
    name = kwargs.get("name")
    dir_ = kwargs.get("dir")
    l = config["project-language"] if not kwargs.get("language") else kwargs.get("language")

    if l == "Python":
        language = "python"
    elif l == "Javascript":
        language = "js"
    elif l == "Golang":
        language = "go"
    else:
        print(f"不支持的默认语言{l}")
        return False
    grpc = kwargs.get("grpc")

    if grpc:
        if language not in ("go", "Go", "golang", "Golang"):
            to = kwargs.get("to") if kwargs.get("to") else config["project-name"]+"/grpc_schema"
            command = f"python -m grpc_tools.protoc -I{dir_} --{language}_out={to} \
                --grpc_{language}_out={to} {name}"
        else:
            to = kwargs.get("to") if kwargs.get("to") else "grpc_schema"
            command = f"protoc -I {dir_} {dir_}/{name} --{language}_out=plugins=grpc:{to}"
    else:
        to = kwargs.get("to") if kwargs.get("to") else "."
        command = f"protoc -I={dir_} --{language}_out={to} {dir_}/{name}"
    if not PROJECT_HOME.joinpath(to).is_dir():
        PROJECT_HOME.joinpath(to).mkdir()
    subprocess.check_call(command, shell=True)
