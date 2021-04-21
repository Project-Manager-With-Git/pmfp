"""ppm test命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import project


class New(EndPoint):
    """根据模板创建项目."""


project_new = project.regist_sub(New)
