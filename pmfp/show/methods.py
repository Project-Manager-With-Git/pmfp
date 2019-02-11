"""show模块的publish接口show."""
from typing import Dict, Any
from ._show_template import show as show_t
from ._show_component import show as show_c


def show(config: Dict[str, Any])->bool:
    """展示模板或组件.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    Returns:
        bool: 成功找到信息并展示则返回True,否则返回False

    """
    if config["type"] == "template":
        return show_t(name=config["name"], language=config["language"], category=config["category"])
    elif config["type"] == "component":
        return show_c(name=config["name"], language=config["language"], category=config["category"])
