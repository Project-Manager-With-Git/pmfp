"""编译python语言模块."""
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.fs_utils import get_abs_path


def unittest_test_go(test_code: str, *,
                     coverage: bool = False,
                     output: str = "doc_unittest",
                     cwd: str = ".") -> None:
    """对python代码做单元测试.

    Args:
        test_code (str): 项目测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        output (Optional[str]): 覆盖率文档位置
        cwd (Optional[str]): 项目的根目录位置

    """
    if cwd:
        cwdp = get_abs_path(cwd)
        test_code_path = get_abs_path(test_code, cwdp)
    else:
        cwdp = Path(".")
        test_code_path = get_abs_path(test_code)
    if coverage:
        if output:
            def coverage_success(_: str) -> None:
                if output:
                    output_path = get_abs_path(output, cwd=cwdp).joinpath("index.html")
                    command = f"go tool cover -html=cover.out -o {str(output_path)}"
                    run_command(command, cwd=cwdp)
                else:
                    warnings.warn("要获得覆盖率文档必须指定输出文档位置")

            command = f"go test -v -coverprofile=cover.out {str(test_code_path)}"
            run_command(
                command, cwd=cwdp, visible=True
            ).catch(lambda _: str(_)).then(
                coverage_success
            ).get()
        else:
            command = f"go test -v -cover {str(test_code_path)}"
            run_command(command, cwd=cwdp, visible=True).catch(lambda _: str(_)).get()
    else:
        command = f"go test -v {str(test_code_path)}"
        run_command(command, cwd=cwdp, visible=True).catch(lambda _: str(_)).get()
