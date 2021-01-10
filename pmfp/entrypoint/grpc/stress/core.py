from schema_entry import EntryPoint
from ..core import grpc


class Stress(EntryPoint):
    """请求指定grpc的服务.

    需要本地有`grpcurl`,可以在`https://github.com/fullstorydev/grpcurl/releases`下载安装
    """
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["url", "method"],
        "properties": {
            "url": {
                "type": "string",
                "description": "grpc的服务位置.",
            },
            "method": {
                "type": "string",
                "description": "请求grpc的方法.",
            },
            "requests": {
                "type": "integer",
                "description": "请求的总次数",
                "default": 100
            },
            "concurrency": {
                "type": "integer",
                "description": "并发量",
                "default": 10
            },
            "duration": {
                "type": "integer",
                "description": "间隔时间,单位s",
                "default": 0
            },
            "payload": {
                "type": "string",
                "description": "请求grpc的负载.",
            },
            "cwd": {
                "type": "string",
                "description": "执行操作时的操作目录.",
                "default": "."
            },
            "plaintext": {
                "type": "boolean",
                "description": "是否不使用TLS加密传输.",
                "default": False
            },
            "insecure": {
                "type": "boolean",
                "description": "跳过服务器证书和域验证.",
                "default": False
            },
            "cacert": {
                "type": "string",
                "description": "根证书位置."
            },
            "cert": {
                "type": "string",
                "description": "服务证书位置."
            },
            "key": {
                "type": "string",
                "description": "服务证书对应的私钥位置."
            },
        }
    }


grpc_stress_test = grpc.regist_sub(Stress)
