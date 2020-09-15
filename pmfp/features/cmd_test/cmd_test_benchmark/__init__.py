"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any, List, Optional
from .test_py import benchmark_test_py
from .test_go import benchmark_test_go


def benchmark_test(language: str, testcode: str, *, root: Optional[str] = None, mem: bool = False) -> None:
    """对指定语言的代码做性能测试.

    Args:
        language (str): 指定的编程语言
        testcode (str): 待测代码
        mem (bool, optional): 是否测试内存性能. Defaults to False.

    """
    if language == "py":
        benchmark_test_py(testcode=testcode, mem=mem, root=root)
    elif language == "go":
        benchmark_test_go(testcode=testcode, mem=mem, root=root)
    else:
        print(f"未支持的语言{language}")
