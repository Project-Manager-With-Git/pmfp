"""ppm requires命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Requires(EntryPoint):
    """管理依赖."""


requires = ppm.regist_sub(Requires)
