from voluptuous import Schema

Schemas = {

}


def register_schema(schema_name: str, *args, **kwargs)->Schema:
    """将定义的schema注册到Schemas表中.

    使用的时候

    >>> register_schema("user",
    ... {
    ...     'name': str,
    ...     'age': int
    ... })

    Args:
        schema_name (str): 

    Returns:
        [Schema]: 格式对象
    """
    schema = Schema(*args, **kwargs)
    Schemas[schema_name] = schema
    return schema
