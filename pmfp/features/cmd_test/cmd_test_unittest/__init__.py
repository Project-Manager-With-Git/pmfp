"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any, List,Optional
from .test_py import unittest_test_py
from .test_go import unittest_test_go

def unittest_test(language: str, testcode: str,*,coverage: Optional[bool],source:Optional[List[str]], output: Optional[str]) -> None:
    """对指定代码做单元测试.

    Args:
        language (str): 目标语言
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置

    """
    if language == "py":
        unittest_test_py(testcode=testcode,coverage=coverage,source=source, output=output)
    elif language == "go":
        unittest_test_go(testcode=testcode,coverage=coverage,source=source, output=output)
    else:
        print(f"未支持的语言{language}")
