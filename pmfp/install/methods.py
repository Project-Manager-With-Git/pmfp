"""为项目安装依赖."""
from typing import Dict, Any
from ._install_js import install as install_j
from ._install_python import install as install_p
from ._install_golang import install as install_g

def install(config: Dict[str, Any], kwargs: Dict[str, Any])->None:
    """为项目安装依赖.

    Args:
        config (Dict[str, Any]): [description]
        kwargs (Dict[str, Any]): [description]
    """
    p_language = config["project-language"]
    if p_language == "Javascript":
        install_j(config=config, **kwargs)
    elif p_language == "Python":
        install_p(config=config, **kwargs)
    elif p_language == "Golang":
        install_g(config=config, **kwargs)
    else:
        print("目前install子命令还不支持{p_language}语言")
