from pathlib import Path
from typing import Optional
from pmfp.const import DEFAULT_AUTHOR
from .build_py import doc_build_py
from .build_go import doc_build_go
from .core import doc_build


@doc_build.as_main
def build_doc(language: str, output: str, doc_source_dir: str, *, version: Optional[str] = None, cwd: str = ".") -> None:
    """为项目构造api文档.
    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        doc_source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
        cwd (str): 执行项目时的位置
    """
    if language == "py":
        doc_build_py(output=output, source_dir=doc_source_dir, version=version, cwd=cwd)
    elif language == "go":
        doc_build_go(output=output, source_dir=doc_source_dir, cwd=cwd)
