from schema_entry import EntryPoint
from ..core import grpc


class Build(EntryPoint):
    """根据grpc的定义protobuf文件编译指定语言的模块.

    需要本地有`protoc`,可以在`https://github.com/protocolbuffers/protobuf/releases`下载安装
    """
    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env", "source_relative", "includes", "files"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            },
            "env": {
                "description": "proto文件名,也是package名",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["py", "js", "go"]
                }
            },
            "to": {
                "type": "string",
                "description": "存放的地方",
                "default": "."
            },
            "source_relative": {
                "type": "boolean",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "includes": {
                "type": "array",
                "description": "待编译的文件的依赖所在的文件夹",
                "items": {
                    "type": "string"
                },
                "default": ["pbschema"]
            },
            "kwargs": {
                "type": "string",
                "description": "其他键值对的额外参数,使用`key::value,key::value`的形式"
            },
            "files": {
                "type": "array",
                "description": "待编译的文件名",
                "items": {
                    "type": "string"
                }
            }
        }
    }


grpc_build = grpc.regist_sub(Build)
