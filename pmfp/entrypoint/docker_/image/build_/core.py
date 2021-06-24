"""ppm docker image build命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockerimage


class Build(EndPoint):
    """由一个dockerfile文件编译镜像."""
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
            "cross_compiling": {
                "type": "boolean",
                "title": "x",
                "default": False,
                "description": "是否交叉编译"
            },
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
            "only_manifest": {
                "type": "boolean",
                "description": "交叉编译时是否直接编译为manifest,为True会执行push操作",
                "default": False
            },
            "push": {
                "type": "boolean",
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


dockerimage_build = dockerimage.regist_sub(Build)
