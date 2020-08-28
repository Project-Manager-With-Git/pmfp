"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any,List,NoReturn
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .build_pb_web import build_pb_web

def _build_pb(env:List[str],files: List[str], includes: List[str], to: str, grpc: bool,source_relative:bool,**kwargs: Dict[str, str]) -> NoReturn:
    if env.lower() == "go":
        build_pb_go(files, includes, to, grpc,source_relative,**kwargs)
    elif env.lower() == "py":
        build_pb_py(files, includes, to, grpc,**kwargs)
    elif env in ("js"):
        build_pb_js(files, includes, to, grpc,**kwargs)
    elif env in ("web"):
        build_pb_web(files, includes, to, grpc,**kwargs)
    else:
        print(f"未知的环境类型{env}")


def build_pb(env:List[str],files: List[str], includes: List[str], to: str, grpc: bool,source_relative:bool, **kwargs: Dict[str, str]) -> NoReturn:
    """编译protobuf的schema为不同语言的代码.

    Args:
        env (List[str]): 编译到的执行环境,可选的有"go","py","js","web"
        files (List[str]): 待编译的文件列表
        includes (List[str]): 待编译文件及其依赖所在文件夹列表
        to (str): 编译到的模块所在文件夹.
        grpc (bool): 是否是grpc
        source_relative (bool): 是否使用路径作为包名,只针对go语言

    """
    if len(env) <=0:
        print("必须至少有一个目标环境")
    else:
        if len(env) == 1:
            _build_pb(env[0],files, includes, to, grpc,source_relative, **kwargs)
        else:
            for e in env:
                new_to = "{to}/{e}"
                _build_pb(e,files, includes, new_to, grpc,source_relative, **kwargs)
    
    
