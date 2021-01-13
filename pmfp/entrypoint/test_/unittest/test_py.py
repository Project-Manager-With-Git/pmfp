"""编译python语言模块."""
import warnings
from pathlib import Path
from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.tools_info_utils import get_local_python, get_global_python
from pmfp.utils.run_command_utils import run_command


def unittest_test_py(test_code: str, code: str, *,
                     coverage: Optional[bool] = False, output: Optional[str] = "doc_unittest", cwd: Optional[str] = ".") -> None:
    """对python代码做单元测试.

    Args:
        test_code (str): 测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        code (Optional[str]): 项目源码
        output (Optional[str]): 覆盖率文档位置
        cwd (Optional[str]): 执行测试时的位置
    """
    if cwd:
        cwdp = get_abs_path(cwd)
        python = get_local_python(cwdp)
        test_code_path = get_abs_path(test_code, cwdp)
    else:
        cwdp = Path(".")
        python = get_global_python()
        test_code_path = get_abs_path(test_code)
    if coverage:
        def coverage_command(_: str) -> None:
            if output:
                output_path = get_abs_path(output, cwdp)
                command = f"{python} -m coverage html -d {str(output_path)}"
            else:
                command = f"{python} -m coverage report"
            print(f"执行命令:{command}")
            return command

        if not code:
            warnings.warn("要获得覆盖率必须指定要覆盖的源码")
            return
        
        command = f"{python} -m coverage run --source={code} -m unittest discover -v -s {str(test_code_path)}"
        print(f"执行命令:{command}")
        run_command(
            command, cwd=cwdp, visible=True
        ).then(
            coverage_command
        ).then(
            lambda command: run_command(command, cwd=cwdp, visible=True)
        ).catch(lambda _: str(_)).get()
    else:
        command = f"{python} -m unittest discover -v -s {str(test_code_path)}"
        print(f"执行命令:{command}")
        run_command(command, cwd=cwdp, visible=True).catch(lambda _: str(_)).get()
