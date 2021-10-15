from typing import Optional
from .build_py import doc_build_py
from .build_go import doc_build_go
from .core import doc_build


@doc_build.as_main
def build_doc(language: str, output: str, *, doc_source_dir: str = "", version: Optional[str] = None, is_web: bool = False, cwd: str = ".") -> None:
    """为项目构造api文档.
    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        doc_source_dir (str): 文档源码位置,注意使用sphinx的比如python含义是那个文档项目的路径,而其他的则是源码路径
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
        is_web (bool): 当language为go且is_web为真时执行`swag init --parseDependency --parseInternal`
        cwd (str): 执行项目时的位置
    """
    if language == "py":
        doc_build_py(output=output, source_dir=doc_source_dir, version=version, cwd=cwd)
    elif language == "go":
        doc_build_go(output=output, source_dir=doc_source_dir, cwd=cwd)
