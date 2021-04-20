"""动态语言做静态类型检测."""
from typing import Dict, Any, List
from .test_py import static_test_py
from .core import test_static


@test_static.as_main
def static_test(language: str, code: str, output: str, *, model: bool = False, coverage: bool = False, cwd: str = ".") -> None:
    """对动态语言做静态类型检验.

    Args:
        language (str): 目标语言
        code (str): 目标检测代码
        model (bool): 目标检测代码是否为模块
        coverage (bool): 是否输出检测的覆盖率文档
        output (str): 覆盖率文档位置
        cwd (str): 执行时的根目录

    """
    if language == "py":
        static_test_py(code=code, model=model, coverage=coverage, output=output, cwd=cwd)
    else:
        print(f"未支持的语言{language}")
