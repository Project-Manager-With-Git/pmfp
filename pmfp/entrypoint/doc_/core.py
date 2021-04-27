"""ppm doc命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Doc(EntryPoint):
    """文档相关的工具."""


doc = ppm.regist_sub(Doc)
