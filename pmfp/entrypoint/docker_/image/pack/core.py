"""ppm docker image pack命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockerimage


class Pack(EndPoint):
    """将多个不同平台的同名镜像打包到同一个manifest list."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "platform": {
                "type": "array",
                "title": "p",
                "description": "目标平台",
                "items": {
                    "type": "string",
                    "enum": ["linux/amd64", "linux/arm64", "linux/riscv64",
                             "linux/ppc64le", "linux/s390x", "linux/386", "linux/arm/v7", "linux/arm/v6"]
                },
                "default": ["linux/amd64", "linux/arm64", "linux/arm/v7"]
            },
            "docker_register": {
                "type": "string",
                "title": "r",
                "description": "docker的镜像仓库位置"
            },
            "docker_register_namespace": {
                "type": "string",
                "title": "s",
                "description": "docker的镜像仓库中的命名空间"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "镜像版本"
            },
            "as_latest_img": {
                "type": "boolean",
                "title": "l",
                "description": "是否打上latest标签",
                "default": False
            },
            "push": {
                "type": "boolean",
                "title": "p",
                "description": "是否编译完后推送去仓库",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "执行位置",
                "default": "."
            },
            "use_sudo": {
                "type": "boolean",
                "description": "使用sudo执行命令",
                "default": False
            },
            "sudo_pwd": {
                "type": "string",
                "description": "使用sudo执行命令的密码"
            }
        }
    }


dockerimage_pack = dockerimage.regist_sub(Pack)
