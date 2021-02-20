"""编译python语言模块."""
import subprocess
from pathlib import Path
from pmfp.utils.run_command_utils import run
from pmfp.utils.fs_utils import get_abs_path_str, get_abs_path


def static_test_py(code: str, model: bool, coverage: bool, output: str, *, cwd: str) -> None:
    """对python代码做静态检测.

    Args:
        code (str): 待检测代码
        model (bool): 是否是模块
        coverage (bool): 是否输出覆盖率文档
        output (str): 覆盖率文档位置
        cwd (str): 执行任务的根目录

    """
    cwdp = get_abs_path(cwd)
    outputp = get_abs_path(output, cwd=cwdp)
    codep = get_abs_path(code, cwd=cwdp)
    command_base = "mypy --ignore-missing-imports --show-column-numbers --follow-imports=silent --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores"
    if model:
        if coverage and output:
            command = command_base + f" --html-report={str(outputp)} -m {str(codep)}"
        else:
            command = command_base + f" -m {str(codep)}"
    else:
        if codep.is_dir():
            if coverage and output:
                command = command_base + f" --scripts-are-modules --html-report={str(outputp)} {str(codep)}"
            else:
                command = command_base + f" --scripts-are-modules {str(codep)}"
        else:
            if coverage and output:
                command = command_base + f" --html-report={str(outputp)} {str(codep)}"
            else:
                command = command_base + f" {str(codep)}"

    run(command, cwd=cwdp, visible=True, fail_exit=True)
