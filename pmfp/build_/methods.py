"""build_模块的public方法."""
from typing import Any, Dict

from ._build_js import build_js
from ._build_python import build_python_app, build_python_module
from ._build_golang import build_go


def build(config: Dict[str, Any], inplace=False, cross=None) -> None:
    """根据项目的信息编译源文件到包或者可执行文件.

    build的语义为建造,即由source组建为production.

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json
        inplace (bool, optional): Defaults to False.
    """
    language = config["project-language"]
    type_ = config["project-type"]
    if language == "Python":
        if type_ == "application":
            build_python_app(config)
        else:
            build_python_module(config, inplace)
    elif language == "Javascript":
        build_js()
    elif language == "Golang":
        build_go(config, cross)
