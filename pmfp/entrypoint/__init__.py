"""命令行执行脚本模块."""
from gevent import monkey
monkey.patch_all()
import sys
from .cmd_help import *
from .cmd_version import *
from .cmd_project import *
from .cmd_stack import *
from .cmd_template import *
from .cmd_proto import *
from .cmd_schema import *
from .cmd_http import *
from .core import ppm


def main(argv=sys.argv[1:]):
    """服务启动入口.

    设置覆盖顺序`环境变量>命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    ppm(argv)
