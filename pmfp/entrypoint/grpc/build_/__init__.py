"""编译grpc的protobuf为不同语言的代码并构造模板."""
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.utils.fs_utils import get_abs_path, get_abs_path_str
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .build_pb_cxx import build_pb_cxx
from .core import grpc_build


def _build_pb(language: str, files: List[str], includes: List[str], to: str, as_type: Optional[List[str]],
              source_relative: bool, cwd: Path, **kwargs: str) -> None:
    if language.lower() == "go":
        build_pb_go(files, includes, to, as_type, source_relative, cwd=cwd, **kwargs)
    elif language.lower() in ("py", "cython"):
        build_pb_py(files, includes, to, as_type, cwd=cwd, **kwargs)
    elif language == "js":
        build_pb_js(files, includes, to, as_type, cwd=cwd, **kwargs)
    elif language == "CXX":
        build_pb_cxx(files, cwd=cwd)
    else:
        print(f"未知的环境类型{language}")


@grpc_build.as_main
def build_grpc(language: str, files: List[str], pb_includes: List[str], to: str,
               source_relative: bool, kwargs: Optional[str] = None,
               cwd: str = ".", as_type: Optional[List[str]] = None) -> None:
    """编译grpc的protobuf的schema为不同语言的代码.

    Args:
        language (List[str]): 编译到的执行环境,可选的有"go","py","js"
        files (List[str]): 待编译的文件列表
        pb_includes (List[str]): 待编译文件及其依赖所在文件夹列表
        to (str): 编译到的模块所在文件夹.
        source_relative (bool): 是否使用路径作为包名,只针对go语言
        kwargs (Optional[str]): Default: None,
        cwd (str): 执行的根目录. Default: "."
        as_type (Optional[List[str]]): 执行的目的,可以是client,service,aioclient,aioserv,nogencli,nogenserv. Default: None

    """
    cwdp = get_abs_path(cwd)
    topath = get_abs_path(to, cwdp)
    if not topath.is_dir():
        topath.mkdir(parents=True)
    files = [file if file.endswith(".proto") else f"{file}.proto" for file in files]
    includes = [get_abs_path_str(i, Path(cwd)) for i in pb_includes]
    if kwargs:
        kwpairs = kwargs.split(",")
        kw = {i.split("::")[0]: i.split("::")[1] for i in kwpairs}
    else:
        kw = {}
    _build_pb(language, files, includes, to, as_type, source_relative, cwd=cwdp, **kw)
