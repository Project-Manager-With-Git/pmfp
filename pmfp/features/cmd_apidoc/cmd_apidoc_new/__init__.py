"""为项目生成api文档."""
from typing import Dict, Any, List, Optional
from .new_py import apidoc_new_py


def new_apidoc(language: str, code: str, output: str, source_dir: str, *, root: str, project_name: str, author: str, version: str) -> None:
    """生成指定代码的api文档.

    Args:
        language (str): 目标项目语言
        code (str): 目标程序源代码
        output (str): 文档位置
        source_dir (str): 文档源码位置
        root (str): 项目根目录
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    if language == "py":
        apidoc_new_py(code=code, output=output, source_dir=source_dir, root=root, project_name=project_name, author=author, version=version)

    else:
        print(f"未支持的语言{language}")
