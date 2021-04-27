"""单元测试."""
from typing import Dict, Any, List, Optional
from .test_py import unittest_test_py
from .test_go import unittest_test_go
from .core import test_unittest


@test_unittest.as_main
def unittest_test(language: str, test_code: str, code: str, *, cwd: str = ".", coverage: bool = False, output: str = "doc_unittest") -> None:
    """对指定代码做单元测试.

    Args:
        language (str): 目标语言
        test_code (str): 测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        code (str): 测试源码
        output (Optional[str]): 覆盖率文档位置
        cwd (str): 执行测试时的位置

    """
    if language == "py":
        unittest_test_py(test_code=test_code, code=code, cwd=cwd, coverage=coverage, output=output)
    elif language == "go":
        unittest_test_go(test_code=test_code, cwd=cwd, coverage=coverage, output=output)
    else:
        print(f"未支持的语言{language}")
