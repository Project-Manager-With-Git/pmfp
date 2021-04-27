"""ppm schema命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Schema(EntryPoint):
    """jsonschema相关的工具."""


schema = ppm.regist_sub(Schema)
