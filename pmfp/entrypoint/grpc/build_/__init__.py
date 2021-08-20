"""编译grpc的protobuf为不同语言的代码并构造模板."""
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.utils.fs_utils import get_abs_path, get_abs_path_str
from .build_pb_go import build_pb_go
from .build_pb_js import build_pb_js
from .build_pb_py import build_pb_py
from .build_pb_cpp import build_pb_cpp
from .core import grpc_build


def _build_pb(language: str, serv_file: str, includes: List[str], to: str,
              go_source_relative: bool,
              js_import_style: str, web_import_style: str, web_mode: str,
              cwd: Path, web: bool = False, files: Optional[List[str]] = None, **kwargs: str) -> None:
    if language.lower() == "go":
        build_pb_go(serv_file, includes, to, go_source_relative, cwd=cwd, files=files, **kwargs)
    elif language.lower() in ("py", "cython"):
        build_pb_py(serv_file, includes, to, cwd=cwd, files=files, **kwargs)
    elif language == "js":
        build_pb_js(serv_file, includes, to, cwd=cwd, files=files,
                    js_import_style=js_import_style,
                    web_import_style=web_import_style,
                    web_mode=web_mode, web=web, **kwargs)
    elif language == "CXX":
        build_pb_cpp(serv_file, includes, to, cwd=cwd, files=files, **kwargs)
    else:
        print(f"未知的环境类型{language}")


@grpc_build.as_main
def build_grpc(language: str, serv_file: str, pb_includes: List[str], to: str,
               js_import_style: str, web_import_style: str, web_mode: str,  
               go_source_relative: bool = False,
               web: bool = False,
               kwargs: Optional[str] = None, files: Optional[List[str]] = None,
               cwd: str = ".") -> None:
    """编译grpc的protobuf的schema为不同语言的代码.

    Args:
        language (List[str]): 编译到的执行环境,可选的有"go","py","js"
        serv_file (str): 服务文件名.
        pb_includes (List[str]): 待编译文件及其依赖所在文件夹列表
        to (str): 编译到的模块所在文件夹.
        source_relative (bool): 是否使用路径作为包名,只针对go语言
        kwargs (Optional[str]): Default: None,
        files (Optional[List[str]]): 待编译的其他文件列表
        cwd (str): 执行的根目录. Default: "."

    """
    cwdp = get_abs_path(cwd)
    topath = get_abs_path(to, cwdp)
    if not topath.is_dir():
        topath.mkdir(parents=True)

    serv_file = serv_file if serv_file.endswith(".proto") else f"{serv_file}.proto"
    if files:
        files = [file if file.endswith(".proto") else f"{file}.proto" for file in files]
    includes = [get_abs_path_str(i, Path(cwd)) for i in pb_includes]
    if kwargs:
        kwpairs = kwargs.split(",")
        kw = {i.split("::")[0]: i.split("::")[1] for i in kwpairs}
    else:
        kw = {}
    _build_pb(language=language,
              serv_file=serv_file,
              includes=includes,
              to=to,
              go_source_relative=go_source_relative,
              js_import_style=js_import_style,
              web_import_style=web_import_style,
              web_mode=web_mode, web=web,
              cwd=cwdp, files=files, ** kw)
