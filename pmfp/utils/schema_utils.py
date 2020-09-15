"""用于检测数据模式的公用组件."""
from typing import Dict, Any
from jsonschema import validate


def is_validated(instance: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """检测数据是否符合模式.

    Args:
        instance (Dict[str,Any]): 待检测数据
        schema (Dict[str,Any]): 需要满足的模式

    Returns:
        bool: 是否通过验证

    """
    try:
        validate(instance=instance, schema=schema)
    except Exception as e:
        print("jsonschema validation not pass.")
        print(str(e))
        return False
    else:
        return True
