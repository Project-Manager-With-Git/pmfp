"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any, List
from .test_py import static_test_py


def static_test(language: str, code: str, model: bool, coverage: bool, output: str, *, root: str) -> None:
    """对动态语言做静态类型检验.

    Args:
        language (str): 目标语言
        code (str): 目标检测代码
        model (bool): 目标检测代码是否为模块
        coverage (bool): 是否输出检测的覆盖率文档
        output (str): 覆盖率文档位置
        root (str): 执行时的根目录

    """
    if language == "py":
        static_test_py(code=code, model=model, coverage=coverage, output=output, root=root)
    else:
        print(f"未支持的语言{language}")
