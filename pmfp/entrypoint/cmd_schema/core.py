"""ppm schema命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_schema = EntryPoint()
ppm_schema.__name__="schema"
ppm_schema.__doc__ = """ppm schema <subcmd>

    ppm schema 的子命令有:

    new                 创建一个json schema的模式文件
    move                将一个存在的json schema模式文件改变位置并更改id.
    check               检查一个json文件是否满足指定的json schema的模式
    test                检查一个json schema的模式文件中的样例是否满足该模式
    """
ppm_schema.prog = "ppm schema"
ppm_schema.epilog = ''
ppm_schema.description = '管理json schema文件的子命令'
ppm.regist_subcmd(ppm_schema)