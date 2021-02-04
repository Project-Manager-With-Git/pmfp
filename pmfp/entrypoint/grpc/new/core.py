from pmfp.utils.endpoint import EndPoint
from ..core import grpc


class New(EndPoint):
    """创建Grpc定义文件."""
    argparse_noflag = "name"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "proto文件名,也是package名"
            },
            "pb_include": {
                "type": "string",
                "title": "t",
                "description": "protobufer文件存放的地方",
                "default": "pbschema"
            },
            "parent_package": {
                "type": "string",
                "title": "p",
                "description": "package父package"
            },
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            }
        }
    }


grpc_new = grpc.regist_sub(New)
