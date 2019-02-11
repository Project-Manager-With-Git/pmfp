"""config模块的通用工具,也是config对外公开的方法."""
import json
from pathlib import Path
from typing import Dict, Any, Union

from pmfp.const import PMFPRC_PATH

from .verify import config_schema


def load_conf(path: Union[Path, str])->Dict[str, Any]:
    """指定地址加载配置文件为配置字典.

    Returns:
        Dict[str, Any]: 项目的配置字典

    """
    with open(str(path), encoding="utf-8") as f:
        result = json.load(f)
    return config_schema(result)


def load_rc()->Dict[str, Any]:
    """读取pmfp.json,获得项目配置.

    Returns:
        Dict[str, Any]: 项目的配置字典

    """
    if PMFPRC_PATH.is_file():
        config = load_conf(PMFPRC_PATH)
        return config
    else:
        return False


def write_rc(config: Dict[str, Any])->None:
    """将项目的配置字典写到配置文件.

    Args:
        config (Dict[str, Any]): 项目的配置字典

    """
    old_conf = load_rc()
    if old_conf:
        old_conf.update(config)
        config = old_conf
    config = config_schema(config)
    with open(str(PMFPRC_PATH), "w", encoding="utf-8") as f:
        json.dump(config, f)
    print("配置文件")
