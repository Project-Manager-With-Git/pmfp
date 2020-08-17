"""project命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_project = EntryPoint()
ppm_project.__doc__ = """ppm project <subcmd>

    ppm project 的子命令有:

    init              初始化一个项目.
    add               新增一个组件
    info              查看项目信息
    update            更新项目
    build             编译项目
    upload            上传项目
    release           发布项目
    clean             清除一个项目
    test              执行测试
    doc               编译文档
    """
ppm_project.__name__="project"
ppm.regist_subcmd(ppm_project)
