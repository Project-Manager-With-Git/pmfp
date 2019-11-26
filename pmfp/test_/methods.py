"""test模块的publish的方法."""

from typing import Dict, Any
from ._js_test import run_js_test
from ._python_test import run_python_test
from ._golang_test import run_golang_test


def test(config: Dict[str, Any], kwargs: Dict[str, Any]) -> bool:
    """测试项目.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        kwargs (Dict[str, Any]): 测试命令字典.

    Returns:
        bool: 是否测试成功

    """
    html = kwargs["html"]
    typecheck = kwargs["typecheck"]
    benchmark = kwargs["benchmark"]
    source = kwargs["source"]
    language = config["project-language"]
    if language == "Python":
        run_python_test(config, html, typecheck, source)
        return True
    elif language == "Javascript":
        run_js_test()
        return True
    elif language == "Golang":
        run_golang_test(config, benchmark)
    else:
        print("未知的编程语言!")
        return False
