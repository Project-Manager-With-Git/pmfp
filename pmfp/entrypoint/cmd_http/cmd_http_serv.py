"""ppm schema new命令的处理."""
import argparse
from .core import ppm_http
from typing import Sequence
from pmfp.features.cmd_http.cmd_http_serv import http_serv


@ppm_http.regist_subcmd
def serv(argv:Sequence[str])->None:
    """ppm http serv [-flags] port

    以指定位置作为http服务的根目录启动一个静态http服务器.
    """
    parser = argparse.ArgumentParser(
        prog='ppm http serv',
        description='启动一个静态http服务器',
        usage= ppm_http.subcmds.get("serv").__doc__
    )
    parser.add_argument("-r", "--root", type=str,default="", help="http服务的根目录")
    parser.add_argument("-b", "--bind", type=str,default="", help="模式的版本")
    parser.add_argument("port",type=str, help="端口名")
    parser.set_defaults(func=cmd_serv_http)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_serv_http(args: argparse.Namespace)->None:
    try:
        http_serv(port=args.port,root=args.root,bind=args.bind)
    except KeyboardInterrupt as kb:
        print("http静态服务关闭")
    except Exception as e:
        raise e
