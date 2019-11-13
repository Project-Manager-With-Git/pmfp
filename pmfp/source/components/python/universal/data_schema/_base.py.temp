from jsonschema import validate
from typing import Dict, Any, Callable
Schemas = {

}


def register_schema(schema_name: str, schema: Dict[str, Any]) -> Callable[[Dict[str, Any]], None]:
    """将定义的schema注册到Schemas表中.

    使用:

    >>> register_schema("user",
    ...  {
    ... "title": "user",
    ... "description": "query user source",
    ... "type": "object",
    ... "properties": {
    ...     "name": {
    ...         "description": "user name",
    ...         "type": "string"
    ...     }, "age": {
    ...         "description": "user age",
    ...         "type": "integer"
    ...     }
    ... },
    ... "required": ["name", "age"]
    ... }

    Args:
        schema_name (str): 判别式的名字.
        schema (Dict[str, Any]): json schema判别式

    """
    Schemas[schema_name] = lambda instance: validate(instance=instance, schema=schema)
