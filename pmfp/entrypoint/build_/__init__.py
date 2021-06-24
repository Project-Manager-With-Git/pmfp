"""编译指定项目.

编译操作只对静态语言有效
"""
import warnings
from pathlib import Path
from typing import Optional, List
from pmfp.utils.fs_utils import get_abs_path
from .build_go import go_build
from .build_py import py_build
from .core import build_cmd


@build_cmd.as_main
def build(language: str, code: str, project_name: str, *,
          output_dir: str = ".",
          upx: bool = False,
          static: bool = True,
          mini: bool = False,
          includes: Optional[List[str]] = None,
          libs: Optional[List[str]] = None,
          lib_dir: Optional[List[str]] = None,
          build_as: str = "exec",
          for_linux_arch: Optional[str] = None,
          pypi_mirror: Optional[str] = None,
          requires: Optional[List[str]] = None,
          cwd: str = ".") -> None:
    """编译指定代码.

    只支持对linux的交叉编译.

    Args:
        language (str): 编译的代码语言,支持go
        code (str): 语言源码位置或者入口文件位置
        project_name (str): 项目名
        output_dir (str): 编译结果放置的目录
        upx (bool, optional): 是否使用upx给可执行文件加壳. Defaults to False.
        static (bool, optional): 是否编译为无依赖的静态文件. Defaults to True.
        mini (bool, optional): 是否最小化编译. Defaults to False.
        includes (Optional[List[str]], optional): 包含的头文件路径. Defaults to None.
        libs (Optional[List[str]], optional): 使用的库名. Defaults to None.
        lib_dir (Optional[List[str]], optional): 使用的库的位置. Defaults to None.
        build_as (str, optional): 编译为的目标,可选有exec(可执行文件),alib(静态库),dlib(动态库). Defaults to "exec".
        for_linux_arch (str, optional): 是否交叉编译支持其他指令集版本的linux,支持amd64和arm64. Defaults to None.
        cwd (str, optional): 执行编译操作时的执行位置. Defaults to ".".
    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")

    if output_dir:
        output_dirp = get_abs_path(output_dir)
    else:
        output_dirp = Path(".")
    if not output_dirp.exists():
        output_dirp.mkdir(parents=True)
    else:
        if not output_dirp.is_dir():
            warnings.warn("输出目录必须是文件夹")
            return
    if language == "go":
        go_build(code=code,
                 project_name=project_name,
                 output_dir=output_dirp,
                 upx=upx,
                 mini=mini,
                 build_as=build_as,
                 for_linux_arch=for_linux_arch,
                 cwd=cwdp)
    elif language == "py":
        py_build(code=code,
                 project_name=project_name,
                 output_dir=output_dirp,
                 cwd=cwdp,
                 pypi_mirror=pypi_mirror,
                 requires=requires,
                 build_as=build_as,
                 static=static,
                 mini=mini)


__all__ = ["build"]