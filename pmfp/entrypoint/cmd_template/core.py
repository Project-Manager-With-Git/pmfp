"""project命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_template = EntryPoint()
ppm_template.__doc__ = """ppm template <subcmd>

    ppm template 的子命令有:

    module              项目模板管理工具
    component           组件模板管理工具
    """
ppm_template.__name__="template"
ppm.regist_subcmd(ppm_template)
