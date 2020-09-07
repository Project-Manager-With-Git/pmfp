"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import run_command


def benchmark_test_go(testcode:str,*,mem:bool=False) -> None:
    """对python代码做静态检测.

    Args:
        code (str): 待检测代码
        model (bool): 是否是模块
        coverage (bool): 是否输出覆盖率文档
        output (str): 覆盖率文档位置

    """
    if mem:
        command = f"go test -v -run=^${testcode} -bench ."
    else:
        command = f"go test -v -benchmem -run=^${testcode} -bench ."
    run_command(command)
