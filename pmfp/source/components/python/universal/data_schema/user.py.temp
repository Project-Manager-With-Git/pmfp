from voluptuous import (
    Length,
    Required,
    All,
    Range
)
from ._base import register_schema

user_schema = register_schema(
    "user",
    {
        Required('name'): All(str, Length(min=1, max=20)),
        Required('age'): All(int, Range(min=1, max=120))
    }
)
