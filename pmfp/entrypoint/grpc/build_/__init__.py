"""编译protobuf的schema为不同语言的代码."""
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.utils.fs_utils import get_abs_path
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .core import grpc_build


def _build_pb(env: str, files: List[str], includes: List[str], to: str, as_type: str,
              source_relative: bool, **kwargs: str) -> None:
    if env.lower() == "go":
        build_pb_go(files, includes, to, as_type, source_relative, **kwargs)
    elif env.lower() == "py":
        build_pb_py(files, includes, to, as_type, **kwargs)
    elif env == "js":
        build_pb_js(files, includes, to, as_type, **kwargs)
    else:
        print(f"未知的环境类型{env}")


@grpc_build.as_main
def build_grpc(env: List[str], files: List[str], includes: List[str], to: str,
               source_relative: bool, kwargs: Optional[str] = None, cwd: str = ".", as_type: str = "source") -> None:
    """编译grpc的protobuf的schema为不同语言的代码.

    Args:
        env (List[str]): 编译到的执行环境,可选的有"go","py","js"
        files (List[str]): 待编译的文件列表
        includes (List[str]): 待编译文件及其依赖所在文件夹列表
        to (str): 编译到的模块所在文件夹.
        source_relative (bool): 是否使用路径作为包名,只针对go语言
        kwargs (Optional[str]): Default: None,
        cwd (str): 执行的根目录. Default: "."
        as_type (str): 执行的目的. Default: "source"

    """
    if len(env) <= 0:
        print("必须至少有一个目标环境")
    else:
        topath = get_abs_path(to, Path(cwd))
        if not topath.is_dir():
            topath.mkdir(parents=True)

        includes = [get_abs_path(i, Path(cwd)) for i in includes]
        if kwargs:
            kwpairs = kwargs.split(",")
            kw = {i.split("::")[0]: i.split("::")[1] for i in kwpairs}
        else:
            kw = {}
        if len(env) == 1:
            _build_pb(env[0], files, includes, to, as_type, source_relative, **kw)
        else:
            for e in env:
                new_to = "{to}/{e}"
                _build_pb(e, files, includes, new_to, as_type, source_relative, **kw)
