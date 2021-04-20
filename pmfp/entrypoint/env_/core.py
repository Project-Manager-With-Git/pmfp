"""ppm env命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Env(EntryPoint):
    """执行环境相关的工具."""


env = ppm.regist_sub(Env)
