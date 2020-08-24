"""project命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_proto = EntryPoint()
ppm_proto.__name__="proto"
ppm_proto.__doc__ = """ppm proto <subcmd>

    ppm proto 的子命令有:

    new                 创建一个protobuf文件
    build               编译protobuf到指定位置      
    """
ppm.prog = "ppm proto"
ppm.epilog = ''
ppm.description = '管理protobuf文件的子命令'
ppm.regist_subcmd(ppm_proto)