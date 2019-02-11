"""获取项目的版本号和状态."""
from typing import Dict, Any


def status(config: Dict[str, Any])->None:
    """[summary]

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    version = config["version"]
    status = config["status"]
    print(f"项目版本号:{version}")
    print(f"项目状态:{status}")
