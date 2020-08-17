"""project命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_stack = EntryPoint()
ppm_stack.__doc__ = """ppm stack <subcmd>

    ppm stack 的子命令有:
    
    info              查看项目组信息
    init              初始化一个项目组.
    add               新增一个项目到项目组
    rm                从项目组删除一个项目
    
    push              上传项目组中的docker镜像
    deploy            使用`meta`项目中的docker-compose文件部署项目组
    doc               编译项目组文档

    一个项目组必须有一个`meta`项目用于维护项目组的部署配置,文档以及数据对接的schema等信息.
    项目组中的增加和删除并不会真的处理文件系统中的内容项目组只是维护路径.
    """
ppm_stack.__name__="project"
ppm.regist_subcmd(ppm_stack)
