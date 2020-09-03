"""ppm schema clone命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_schema.cmd_schema_clone import clone_schema
from .core import ppm_schema


@ppm_schema.regist_subcmd
def clone(argv: Sequence[str]) -> None:
    """克隆json schema模式文本.

    ppm schema clone [-flags] url
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema clone',
        description='克隆json schema文本',
        usage=ppm_schema.subcmds.get("clone").__doc__
    )
    parser.add_argument("-o", "--out", type=str,
                        default=".", help="输出位置")
    parser.add_argument("-m", "--method", type=str,
                        choices=("GET", "POST"), default="GET", help="http方法")
    parser.add_argument("-a", "--auth", type=str,
                        help="认证字符串,多字段的使用,分隔")
    parser.add_argument("--auth_type", type=str,
                        choices=("basic", "digest", "jwt", "oauth1"), help="认证类型")
    parser.add_argument("-p", "--payload", type=str,
                        help="请求的负载,需要指定json文件")
    parser.add_argument("-t", "--payload_type", type=str,
                        choices=("form", "json", "url"), default="json", help="负载的类型")
    parser.add_argument("--verify", action="store_true",
                        help="https请求是否进行ssl验证")
    parser.add_argument("--cert", type=str,
                        help="指定一个本地证书用作客户端证书,如果是证书加key的形式,可以用','隔开")
    parser.add_argument("url", type=str,
                        help="url地址")
    parser.set_defaults(func=cmd_clone_schema)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_clone_schema(args: argparse.Namespace) -> None:
    """克隆一个远程的json schema文件."""
    clone_schema(
        url=args.url,
        method=args.method,
        out=args.out,
        auth=args.auth,
        auth_type=args.auth_type,
        payload=args.payload,
        payload_type=args.payload_type,
        verify=args.verify,
        cert=args.cert)
