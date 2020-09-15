"""编译python语言模块."""
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run_command, default_succ_cb
from pmfp.utils.fs_utils import get_abs_path


def unittest_test_go(testcode: str, *,
                     coverage: Optional[bool],
                     output: Optional[str],
                     root: Optional[str] = None) -> None:
    """对python代码做单元测试.

    Args:
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        output (Optional[str]): 覆盖率文档位置
        root (Optional[str]): 项目的根目录位置

    """
    if root:
        rootp = get_abs_path(root)
        test_code_path = get_abs_path(testcode, rootp)
    else:
        rootp = Path(".")
        test_code_path = get_abs_path(testcode)
    if coverage:
        if output:
            def coverage_success(content: str) -> None:
                default_succ_cb(content)
                if output:
                    output_path = get_abs_path(output, root=rootp).joinpath("index.html")
                    command = f"go tool cover -html=cover.out -o {str(output_path)}"
                    run_command(command, cwd=rootp)
                else:
                    warnings.warn("要获得覆盖率文档必须指定输出文档位置")
                    return

            command = f"go test -v -coverprofile=cover.out {str(test_code_path)}"
            run_command(command, cwd=rootp, succ_cb=coverage_success)
        else:
            command = f"go test -v -cover {str(test_code_path)}"
            run_command(command, cwd=rootp)
    else:
        command = f"go test -v {str(test_code_path)}"
        run_command(command, cwd=rootp)
