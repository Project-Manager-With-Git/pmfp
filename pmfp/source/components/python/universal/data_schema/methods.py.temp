from ._base import Schemas
from typing import Dict, Any, Callable
from .user import *


def get_schema(schema_name: str) -> Callable[[Dict[str, Any]], None]:
    """获取注册的格式对象.

    Args:
        schema_name (str): 格式名

    Returns:
        [Schema]: 格式对象
    """
    return Schemas.get(schema_name)
