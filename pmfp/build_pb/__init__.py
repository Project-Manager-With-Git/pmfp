"""编译protobuf的schema为不同语言的代码."""
import subprocess
import warnings
from typing import Dict, Any
import chardet
from pmfp.const import PROJECT_HOME
from .build_pb_aio import build_pb_aio
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .build_pb_web import build_pb_web


def build_pb(kwargs: Dict[str, Any]) -> None:
    """编译protobuf的schema为不同语言的代码.

    Args:
        kwargs (Dict[str, Any]): 编译的配置信息字典.
    """
    name = kwargs.get("name")
    dir_ = kwargs.get("dir")
    to = kwargs.get("to")
    language = kwargs.get("language")
    grpc = kwargs.get("grpc")
    if not PROJECT_HOME.joinpath(to).is_dir():
        PROJECT_HOME.joinpath(to).mkdir()

    if language in ("go", "Go", "golang", "Golang"):
        build_pb_go(name, dir_, to, grpc)
    elif language in ("python", "py", "Python", "PY"):
        build_pb_py(name, dir_, to, grpc)
    elif language in ("js", "javascript", "JS", "Javascript"):
        build_pb_js(name, dir_, to, grpc)
    elif language in ("web", "WEB", "Web"):
        if grpc is False:
            print("Asyncio 只有grpc模式")
        else:
            build_pb_web(name, dir_, to, grpc)
    elif language in ("asyncio", "Asyncio", "aio"):
        if grpc is False:
            print("Asyncio 只有grpc模式")
        else:
            build_pb_aio(name, dir_, to, grpc)
