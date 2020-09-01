"""ppm schema new命令的处理."""
import argparse
from .core import ppm_http
from typing import Sequence
from pmfp.features.cmd_http.cmd_http_test import http_test


@ppm_http.regist_subcmd
def test(argv:Sequence[str])->None:
    """ppm http test -s <schema> [--flag] <url>

    检查http请求返回的数据是否满足json schema定义的模式.
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema test',
        description='检查json schema文件',
        usage= ppm_http.subcmds.get("test").__doc__
    )
    parser.add_argument("--schema", type=str,required=True,help="用于验证的json schema,可以是路径也可以是url")
    parser.add_argument("--serialization", type=str,choices=("json",), default="json",help="请求的返回值序列化协议.默认json")
    parser.add_argument("-m", "--method", type=str, choices=("GET","POST","PUT","DELETE"), default="GET",help="请求的http方法")
    parser.add_argument("-a", "--auth", type=str, help="认证字符串,多字段的使用,分隔")
    parser.add_argument("--auth_type", type=str,choices=("basic","digest","jwt","oauth1"), help="认证类型")
    parser.add_argument("-p", "--payload", type=str, help="请求的负载,需要指定json文件")
    parser.add_argument("-t", "--payload_type", type=str,choices=("form","json","url","stream"),default="json", help="负载的类型")
    parser.add_argument("-s", "--stream", action="store_true", help="返回是否为流")
    parser.add_argument("--verify", action="store_true", help="https请求是否进行ssl验证")
    parser.add_argument("--cert", type=str, help="指定一个本地证书用作客户端证书,如果是证书加key的形式,可以用','隔开")
    parser.add_argument("url",type=str, help="请求的路径")
    parser.set_defaults(func=cmd_test_http)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_test_http(args: argparse.Namespace)->None:
    http_test(
        schema=args.schema,
        serialization=args.serialization,
        url=args.url,
        method=args.method,
        auth=args.auth,
        auth_type=args.auth_type,
        payload=args.payload,
        payload_type=args.payload_type,
        stream=args.stream,
        verify=args.verify,
        cert=args.cert)
