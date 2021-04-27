"""ppm test命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Project(EntryPoint):
    """项目管理相关的工具."""


project = ppm.regist_sub(Project)
