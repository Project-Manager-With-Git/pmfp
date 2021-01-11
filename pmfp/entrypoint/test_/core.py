"""ppm test命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Test(EntryPoint):
    """测试相关的工具."""


test = ppm.regist_sub(Test)
