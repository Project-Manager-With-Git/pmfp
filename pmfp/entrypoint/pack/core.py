"""ppm pack命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Pack(EntryPoint):
    """编译指定位置项目."""


env = ppm.regist_sub(Pack)
