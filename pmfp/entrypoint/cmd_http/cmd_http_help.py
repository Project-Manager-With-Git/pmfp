"""ppm http help命令的处理."""
import argparse
from .core import ppm_http
from typing import Sequence


@ppm_http.regist_subcmd
def help(argv:Sequence[str])->None:
    """ppm http help <subcommand>
ppm http 的子命令有:

    serv                创建一个静态http服务
    get                 使用get方法访问一个http服务上的资源
    post                使用post方法访问一个http服务上的资源
    put                 使用put方法访问一个http服务上的资源
    delete              使用delete方法访问一个http服务上的资源
    stress              压测一个http接口
    test                检查一个http接口是否符合指定json schema的模式文件中定义的模式
    """
    parser = argparse.ArgumentParser(
        prog='ppm http help',
        description='查看子命令的帮助说明',
        usage= ppm_http.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_http.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)

def cmd_help(args:argparse.Namespace)->None:
    print(ppm_http.subcmds.get(args.subcmd).__doc__)