"""编译protobuf的schema为不同语言的代码."""
import subprocess
import warnings
from typing import Dict, Any,List
import chardet
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .build_pb_web import build_pb_web


def build_pb(language:str,files: List[str], includes: List[str], to: str, grpc: bool, **kwargs: Dict[str, str]) -> None:
    """编译protobuf的schema为不同语言的代码.
    Args:
        kwargs (Dict[str, Any]): 编译的配置信息字典.
    """
    if language.lower() == "golang":
        build_pb_go(files, includes, to, grpc,**kwargs)
    elif language.lower() == "python":
        build_pb_py(name, dir_, to, grpc)
    elif language in ("js", "javascript", "JS", "Javascript"):
        build_pb_js(name, dir_, to, grpc)
    elif language in ("web", "WEB", "Web"):
        if grpc is False:
            print("Asyncio 只有grpc模式")
        else:
            build_pb_web(name, dir_, to, grpc)
    
