"""new模块的通用工具."""
import json
from typing import Dict, Any
from pmfp.const import (
    JS_ENV_PATH
)


def new_json_package(config: Dict[str, Any])->None:
    """创建package.json.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    if not JS_ENV_PATH.exists():
        with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
            content = {
                "name": config["project-name"],
                "version": config["version"],
                "description": config["description"],
                "author": config["author"],
                "license": config["license"]
            }
            json.dump(content, f)
