"""ppm docker image new命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockerimage


class New(EndPoint):
    """创建一个dockerfile文件."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "dockerfile_name": {
                "type": "string",
                "title": "f",
                "description": "dockerfile名字",
                "default": "Dockerfile"
            },
            "language": {
                "description": "目标语言使用的dockerfile",
                "title": "l",
                "type": "string",
                "enum": ["py", "cython", "go", "CXX"]
            },
            "cross_compiling": {
                "type": "boolean",
                "title": "x",
                "description": "是否交叉编译",
                "default": False
            },
            "app_name": {
                "description": "项目名",
                "title": "a",
                "type": "string"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "extend": {
                "description": "是否使用c扩展",
                "type": "boolean",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "执行位置",
                "default": "."
            }
        }
    }


dockerfile_new = dockerimage.regist_sub(New)
