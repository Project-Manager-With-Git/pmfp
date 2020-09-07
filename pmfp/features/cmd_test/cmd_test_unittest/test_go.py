"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import run_command,default_succ_cb
from typing import List,Optional

def unittest_test_go(testcode: str,*,coverage: Optional[bool],source:Optional[List[str]], output: Optional[str]) -> None:
    """对python代码做单元测试.

    Args:
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置

    """
    if coverage:
        if output:
            def coverage_success(content:str)->None:
                default_succ_cb(content)
                command = "go tool cover -html=cover.out -o {output}/index.html"
                run_command(command)

            command = "go test -v -coverprofile=cover.out {testcode}"
            run_command(command,succ_cb=coverage_success)
        else:
            command = "go test -v -cover {testcode}"
            run_command(command)
    else:
        command = "go test -v {testcode}"
        run_command(command)
