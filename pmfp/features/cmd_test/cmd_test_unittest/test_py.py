"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import run_command,default_succ_cb,get_local_python_path
from typing import List,Optional

def unittest_test_py(testcode: str,*,coverage: Optional[bool],source:Optional[List[str]], output: Optional[str]) -> None:
    """对python代码做单元测试.

    Args:
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置

    """
    python = get_local_python_path()
    if coverage:
        def coverage_success(content:str)->None:
            default_succ_cb(content)
            if output:
                command = f"{python} -m coverage html -d {output}"
            else:
                command = f"{python} -m coverage report"
            run_command(command)

        sources = ",".join(source)
        command = f"{python} -m coverage run --source={sources} -m unittest discover -v -s {testcode}"
        run_command(command,succ_cb=coverage_success)
    else:
        command = f"{python} -m unittest discover -v -s {testcode}"
        run_command(command)
