"""性能基准测试."""
from typing import Dict, Any, List, Optional
from .test_py import benchmark_test_py
from .test_go import benchmark_test_go
from .core import test_benchmark


@test_benchmark.as_main
def benchmark_test(language: str, benchmark_code: str, *, cwd: Optional[str] = None, mem: bool = False) -> None:
    """对指定语言的代码做性能测试.

    Args:
        language (str): 指定的编程语言
        benchmark_code (str): 待测代码
        mem (bool, optional): 是否测试内存性能. Defaults to False.
        cwd (Optional[str]): 执行时的根目录. Defaults to None.

    """
    if language == "py":
        benchmark_test_py(benchmark_code=benchmark_code, mem=mem, cwd=cwd)
    elif language == "go":
        benchmark_test_go(benchmark_code=benchmark_code, mem=mem, cwd=cwd)
    else:
        print(f"未支持的语言{language}")
