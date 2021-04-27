"""编译python语言模块."""
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run
from pmfp.utils.fs_utils import get_abs_path


def benchmark_test_go(benchmark_code: str, *, cwd: Optional[str] = None, mem: bool = False) -> None:
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

    if mem:
        command = f"go test -v -run=^${benchmark_code} -bench ."
    else:
        command = f"go test -v -benchmem -run=^${benchmark_code} -bench ."
    run(command, cwd=cwdp, visible=True, fail_exit=True)
