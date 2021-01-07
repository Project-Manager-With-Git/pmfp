"""ppm proto new命令的处理."""
# import argparse
# from typing import Sequence
# from pmfp.features.cmd_proto.cmd_proto_new import new_pb
from schema_entry import EntryPoint
from .core import proto


class New(EntryPoint):
    """创建protobuf文件."""
    argparse_noflag = "name"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "proto文件名,也是package名"
            },
            "grpc": {
                "type": "boolean",
                "description": "是否是grpc"
            },
            "to": {
                "type": "string",
                "description": "存放的地方",
                "default": "."
            },
            "parent_package": {
                "type": "string",
                "description": "package父package"
            },
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            }
        }
    }


proto_new = proto.regist_sub(New)
