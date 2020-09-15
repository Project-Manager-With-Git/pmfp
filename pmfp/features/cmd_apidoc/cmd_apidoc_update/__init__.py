"""更新不同语言的api文档."""
from typing import Dict, Any, List, Optional
from .update_py import apidoc_update_py


def update_apidoc(language: str, code: str, output: str, source_dir: str, *, root: str) -> None:
    """更新不同语言的api文档.

    Args:
        language (str): 指定的编程语言
        code (str): 项目的源码位置
        output (str): 文档所在文件夹
        source_dir (str): 文档源码文件夹
        root (str): 项目根目录

    """
    if language == "py":
        apidoc_update_py(code=code, output=output, root=root, source_dir=source_dir)

    else:
        print(f"未支持的语言{language}")
