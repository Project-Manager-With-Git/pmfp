"""ppm docker file new命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockerfile


class New(EndPoint):
    """创建一个dockerfile文件."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["cwd"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "执行位置",
            },
            "cross_compiling": {
                "type": "boolean",
                "title": "x",
                "description": "是否交叉编译"
            },
            "file_name": {
                "type": "string",
                "title": "f",
                "description": "dockerfile名字"
            }
        }
    }


dockerfile_new = dockerfile.regist_sub(New)
