"""ppm http命令的处理."""
import argparse
from ..core import ppm,EntryPoint
from typing import Sequence

ppm_http = EntryPoint("http")
ppm_http.__doc__ = """ppm http <subcmd>

    ppm http 的子命令有:

    serv                创建一个静态http服务
    get                 使用get方法访问一个http服务上的资源
    post                使用post方法访问一个http服务上的资源
    put                 使用put方法访问一个http服务上的资源
    delete              使用delete方法访问一个http服务上的资源
    stress              压测一个http接口
    test                检查一个http接口是否符合指定json schema的模式文件中定义的模式
    """
ppm_http.prog = "ppm http"
ppm_http.epilog = ''
ppm_http.description = 'http相关的子命令'
ppm.regist_subcmd(ppm_http)