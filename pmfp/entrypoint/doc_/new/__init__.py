import warnings
from pathlib import Path
from typing import Optional
from pmfp.const import DEFAULT_AUTHOR
from .new_py import doc_new_py
from .new_go import doc_new_go
from .core import doc_new


@doc_new.as_main
def new_doc(language: str, code: str, output: str, doc_source_dir: str, *,
            project_name: Optional[str] = None, author: Optional[str] = None, version: Optional[str] = None, cwd: str = ".") -> None:
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
    if not author:
        author = DEFAULT_AUTHOR
    if not project_name:
        project_name = Path(cwd).resolve().name
    if not version:
        version = "0.0.0"
    if language == "py":
        doc_new_py(code=code, output=output, source_dir=doc_source_dir, project_name=project_name, author=author, version=version, cwd=cwd)
    elif language == "go":
        doc_new_go(code=code, output=output, source_dir=doc_source_dir, project_name=project_name, author=author, version=version, cwd=cwd)
    else:
        warnings.warn(f"不支持的语言{language}")
