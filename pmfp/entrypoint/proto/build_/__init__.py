"""编译protobuf的schema为不同语言的代码."""
from pathlib import Path
from typing import Dict, Any, List, Optional
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from schema_entry import EntryPoint
from pmfp.utils.fs_utils import get_abs_path

from ..core import proto

class Build(EntryPoint):
    """创建protobuf文件."""
    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required":["env","grpc","source_relative","includes","files"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            },
            "env": {
                "description": "proto文件名,也是package名",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum":["py","js","go"]
                }
            },
            "grpc": {
                "type": "boolean",
                "description": "是否是grpc",
                "default": False
            },
            "to": {
                "type": "string",
                "description": "存放的地方",
                "default": "."
            },
            "source_relative": {
                "type": "boolean",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "includes":{
                "type": "array",
                "description": "待编译的文件的依赖所在的文件夹",
                "items": {
                    "type": "string"
                },
                "default":["pbschema"]
            },
            "kwargs":{
                "type": "string",
                "description": "其他键值对的额外参数,使用`key::value,key::value`的形式"
            },
            "files":{
                "type": "array",
                "description": "待编译的文件名",
                "items": {
                    "type": "string"
                }
            }
        }
    }


proto_build = proto.regist_sub(Build)

def _build_pb(env: str, files: List[str], includes: List[str], to: str, grpc: bool,
              source_relative: bool, **kwargs: str) -> None:
    if env.lower() == "go":
        build_pb_go(files, includes, to, grpc, source_relative, **kwargs)
    elif env.lower() == "py":
        build_pb_py(files, includes, to, grpc, **kwargs)
    elif env == "js":
        build_pb_js(files, includes, to, grpc, **kwargs)
    else:
        print(f"未知的环境类型{env}")

@proto_build.as_main
def build_pb(env: List[str], files: List[str],includes: List[str] , to: str, grpc: bool,
             source_relative: bool, kwargs: Optional[str]=None,cwd:str=".") -> None:
    """编译protobuf的schema为不同语言的代码.

    Args:
        env (List[str]): 编译到的执行环境,可选的有"go","py","js"
        files (List[str]): 待编译的文件列表
        includes (List[str]): 待编译文件及其依赖所在文件夹列表
        to (str): 编译到的模块所在文件夹.
        grpc (bool): 是否是grpc
        source_relative (bool): 是否使用路径作为包名,只针对go语言
        kwargs (Optional[str]): Default: None,
        cwd (str): 执行的根目录. Default: "."
    """
    if len(env) <= 0:
        print("必须至少有一个目标环境")
    else:
        topath = get_abs_path(to,Path(cwd))
        if not topath.is_dir():
            topath.mkdir(parents=True)

        includes = [get_abs_path(i,Path(cwd)) for i in includes]
        if kwargs:
            kwpairs = kwargs.split(",")
            kw = {i.split("::")[0]:i.split("::")[1] for i in kwpairs}
        else:
            kw={}
        if len(env) == 1:
            _build_pb(env[0], files, includes, to, grpc, source_relative, **kw)
        else:
            for e in env:
                new_to = "{to}/{e}"
                _build_pb(e, files, includes, new_to, grpc, source_relative, **kw)
