"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.fs_utils import get_abs_path
from typing import List, Optional,Dict

def static_test_py(code:str,model: bool, coverage:bool,output:str) -> None:
    """对python代码做静态检测

    Args:
        code (str): 待检测代码
        model (bool): 是否是模块
        coverage (bool): 是否输出覆盖率文档
        output (str): 覆盖率文档位置
    """
    if model:
        if coverage and output:
            command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores --html-report={output} -m {code}"
        else:
            command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores -m {code}"
    else:
        if Path(code).is_dir():
            if coverage and output:
                command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores --scripts-are-modules --html-report={output} {code}"
            else:
                command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores --scripts-are-modules {code}"
        else:
            if coverage and output:
                command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores --html-report={output} {code}"
            else:
                command = f"mypy --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs --no-implicit-optional --warn-unused-ignores {code}"
    run_command(command)