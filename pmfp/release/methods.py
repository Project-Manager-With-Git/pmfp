"""发布项目到合适的地方."""
from typing import Dict, Any
from ._release_js import release_js
from ._release_python import release_py


def release(config: Dict[str, Any])->None:
    """发布项目到合适的地方.

    Args:
        config (Dict[str, Any]): 项目的配置字典
    """
    p_language = config["project-language"]
    if p_language == "Javascript":
        release_js(config=config)
    elif p_language == "Python":
        release_py(config=config)
    elif p_language == "Golang":
        release_golang(config=config)
    else:
        print("目前release子命令还不支持{p_language}语言")
