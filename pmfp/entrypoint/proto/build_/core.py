from pmfp.utils.endpoint import EndPoint
from ..core import proto


class Build(EndPoint):
    """创建protobuf文件.
    需要本地有`protoc`,可以在`https://github.com/protocolbuffers/protobuf/releases`下载安装
    """
    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["language", "pb_includes", "files"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            },
            "language": {
                "description": "proto文件名,也是package名",
                "title": "l",
                "type": "string",
                "enum": ["py", "cython", "js", "go", "CXX"]
            },
            "to": {
                "type": "string",
                "title": "t",
                "description": "存放的地方",
                "default": "."
            },
            "pb_includes": {
                "type": "array",
                "title": "i",
                "description": "待编译的protobu文件及其依赖所在的文件夹",
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
            },
            "go_source_relative": {
                "type": "boolean",
                "title": "s",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "js_import_style": {
                "type": "string",
                "description": "编译出来的js模块形式",
                "enum": ["commonjs", "closure"],
                "default": "commonjs"
            }
        }
    }


proto_build = proto.regist_sub(Build)
