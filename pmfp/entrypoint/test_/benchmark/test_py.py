"""编译python语言模块."""
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_local_python
from pmfp.utils.fs_utils import get_abs_path


def benchmark_test_py(benchmark_code: str, *, cwd: Optional[str] = None, mem: bool = False) -> None:
    """对python代码做静态检测.

    Args:
        benchmark_code (str): 待检测测试代码
        model (bool): 是否是模块
        coverage (bool): 是否输出覆盖率文档
        output (str): 覆盖率文档位置

    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")
    python = get_local_python(cwdp)
    if mem:
        command = f"{python} -m kernprof -l -v {benchmark_code}"
    else:
        command = f"{python} -m memory_profiler {benchmark_code}"
    run(command, cwd=cwdp, visible=True, fail_exit=True)
