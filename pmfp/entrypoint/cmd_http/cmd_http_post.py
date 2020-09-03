"""ppm http post命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_http.cmd_http_query import http_query
from .core import ppm_http


@ppm_http.regist_subcmd
def post(argv: Sequence[str]) -> None:
    """使用POST方法访问一个http资源.
    
    ppm http post [-flags] url
    """
    parser = argparse.ArgumentParser(
        prog='ppm http post',
        description='使用post方法访问http服务器上的资源',
        usage=ppm_http.subcmds.get("post").__doc__
    )
    parser.add_argument("-a", "--auth", type=str,
                        help="认证字符串,多字段的使用,分隔")
    parser.add_argument("--auth_type", type=str,
                        choices=("basic", "digest", "jwt", "oauth1"), help="认证类型")
    parser.add_argument("-p", "--payload", type=str,
                        help="请求的负载,需要指定json文件")
    parser.add_argument("-t", "--payload_type", type=str,
                        choices=("form", "json", "url", "stream"), default="json", help="负载的类型")
    parser.add_argument("-s", "--stream", action="store_true",
                        help="返回是否为流")
    parser.add_argument("--verify", action="store_true",
                        help="https请求是否进行ssl验证")
    parser.add_argument("--cert", type=str,
                        help="指定一个本地证书用作客户端证书,如果是证书加key的形式,可以用','隔开")
    parser.add_argument("url", type=str,
                        help="url地址")
    parser.set_defaults(func=cmd_post_http)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_post_http(args: argparse.Namespace) -> None:
    """Post query."""
    http_query(
        url=args.url,
        method="GET",
        auth=args.auth,
        auth_type=args.auth_type,
        payload=args.payload,
        payload_type=args.payload_type,
        stream=args.stream,
        verify=args.verify,
        cert=args.cert,
        cb=print)
