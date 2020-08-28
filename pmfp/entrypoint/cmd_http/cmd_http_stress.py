"""ppm schema new命令的处理."""
import argparse
import json
from .core import ppm_http
from typing import Sequence
from pmfp.features.cmd_http.cmd_http_stress import http_stress


@ppm_http.regist_subcmd
def stress(argv:Sequence[str]):
    """ppm http stress [-flags] port

    对一个http资源做压测,注意参数的优先级命令行>配置文件>默认配置.

    默认配置为:


    """
    parser = argparse.ArgumentParser(
        prog='ppm http stress',
        description='对一个http资源做压测',
        usage= ppm_http.subcmds.get("stress").__doc__
    )
    parser.add_argument("-r", "--requests", type=int,default=100, help="请求的总次数")
    parser.add_argument("-c", "--concurrency", type=int,default=10, help="并发量")
    parser.add_argument("-d", "--duration", type=int,default=0, help="间隔时间s")
    parser.add_argument("-m", "--method", type=str,default="GET",choices=("GET","POST","PUT","DELETE"), help="http方法")
    parser.add_argument("-D", "--data", type=str, help="请求的负载")
    parser.add_argument("-t", "--ct", type=str,default='text/plain',choices=("text/plain","application/json"), help="请求的负载类型")
    parser.add_argument("-q", "--quiet", action="store_true",help="安静执行")
    parser.add_argument("-f", "--config", type=str, help="配置文件")
    parser.add_argument("url",type=str, help="指定要压测的url")
    parser.set_defaults(func=cmd_stress_http)
    args = parser.parse_args(argv)
    args.func(args)

default_config = {
    "requests":100,
    "concurrency":10,
    "duration":0,
    "method":"GET",
    "data":None,
    "ct":'text/plain',
    "auth":None,
    "headers":None,
    "pre_hook":None,
    "post_hook":None,
    "quiet":False
}

def cmd_stress_http(args: argparse.Namespace):
    config = {
    }
    params = vars(args)
    del params["func"]
    config.update(default_config)
    if args.config:
        with open(args.config) as f:
            c = json.load(f)
            config.update(c)
    del params["config"]
    config.update(params)
    http_stress(config)
