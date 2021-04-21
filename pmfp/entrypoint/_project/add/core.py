"""ppm test命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Add(EndPoint):
    """为项目添加组件."""


env = ppm.regist_sub(Add)
