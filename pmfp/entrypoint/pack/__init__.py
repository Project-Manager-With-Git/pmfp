"""打包指定项目.

打包操作只对静态语言有效
"""
import warnings
from pathlib import Path
from typing import Optional, List
from pmfp.utils.fs_utils import get_abs_path
from .pack_py import py_pack
from .core import pack_cmd


@pack_cmd.as_main
def build(language: str, code: str, project_name: str, *,
          output_dir: str = ".",
          pypi_mirror: Optional[str] = None,
          build_as: str = "exec",
          cwd: str = ".") -> None:
    """编译指定代码.

    只支持对linux的交叉编译.

    Args:
        language (str): 打包的代码语言,支持py
        code (str): 语言源码位置或者入口文件位置
        project_name (str): 项目名
        output_dir (str): 打包结果放置的目录
        pypi_mirror (str, optional): 安装python依赖时使用的pypi的镜像
        build_as (str, optional): 编译为的目标,可选有exec(可执行文件),lib(库). Defaults to "exec".
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
        py_pack(code=code,
                project_name=project_name,
                output_dir=output_dirp,
                pypi_mirror=pypi_mirror,
                build_as=build_as,
                cwd=cwdp)
