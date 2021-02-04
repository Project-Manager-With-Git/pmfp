"""ppm docker file build命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockerfile


class Build(EndPoint):
    """由一个dockerfile文件编译镜像."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["cwd"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "执行位置",
            },
            "file_name": {
                "type": "string",
                "title": "f",
                "description": "dockerfile名字"
            },
            "platform": {
                "type": "array",
                "title": "p",
                "description": "目标平台",
                "items": {
                    "type": "string",
                    "enum": ["linux/amd64", "linux/arm64", "linux/riscv64", "linux/ppc64le", "linux/s390x", "linux/386", "linux/arm/v7", "linux/arm/v6"]
                },
                "default": ["linux/amd64", "linux/arm64", "linux/arm/v7"]
            },
            "docker_register": {

            },
            "docker_register_namespace": {

            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "文档源码位置"
            },
            "author": {
                "type": "string",
                "title": "a",
                "description": "文档源码位置"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "文档源码位置"
            },
            "as_latest_img": {
                "type": "boolean",
                "title": "l",
                "description": "是否打上latest标签"
            },
            "push": {
                "type": "boolean",
                "title": "p",
                "description": "是否编译完后推送去仓库"
            }
        }
    }


dockerfile_build = dockerfile.regist_sub(Build)
