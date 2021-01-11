"""编译python语言模块."""
import warnings
from pathlib import Path
from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.tools_info_utils import get_local_python, get_global_python
from pmfp.utils.run_command_utils import run_command


def unittest_test_py(code: str, source: Optional[List[str]], *,
                     coverage: Optional[bool] = False, output: Optional[str] = "doc_unittest", cwd: Optional[str] = ".") -> None:
    """对python代码做单元测试.

    Args:
        code (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置
        cwd (Optional[str]): 执行测试时的位置
    """
    if cwd:
        cwdp = get_abs_path(cwd)
        python = get_local_python(cwdp)
        test_code_path = get_abs_path(code, cwdp)
    else:
        cwdp = Path(".")
        python = get_global_python()
        test_code_path = get_abs_path(code)
    if coverage:
        def coverage_success(_: str) -> None:
            if output:
                output_path = get_abs_path(output, cwdp)
                command = f"{python} -m coverage html -d {str(output_path)}"
            else:
                command = f"{python} -m coverage report"
            run_command(command, cwd=cwdp)
        if not source or len(source) == 0:
            warnings.warn("要获得覆盖率必须指定要覆盖的源码")
            return
        sources = ",".join(source)
        command = f"{python} -m coverage run --source={sources} -m unittest discover -v -s {str(test_code_path)}"
        run_command(
            command, cwd=cwdp, visible=True
        ).then(coverage_success).get()
    else:
        command = f"{python} -m unittest discover -v -s {str(test_code_path)}"
        run_command(command, cwd=cwdp, visible=True).get()
