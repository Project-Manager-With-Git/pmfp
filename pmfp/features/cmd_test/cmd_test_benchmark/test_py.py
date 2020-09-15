"""编译python语言模块."""
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run_command, get_local_python
from pmfp.utils.fs_utils import get_abs_path


def benchmark_test_py(testcode: str, *, root: Optional[str] = None, mem: bool = False) -> None:
    """对python代码做静态检测.

    Args:
        code (str): 待检测代码
        model (bool): 是否是模块
        coverage (bool): 是否输出覆盖率文档
        output (str): 覆盖率文档位置

    """
    if root:
        rootp = get_abs_path(root)
    else:
        rootp = Path(".")
    env_dir = rootp.joinpath("env")
    python = get_local_python(env_dir)
    if mem:
        command = f"{python} -m kernprof -l -v {testcode}"
    else:
        command = f"{python} -m memory_profiler {testcode}"
    run_command(command)
