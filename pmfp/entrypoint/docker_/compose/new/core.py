"""ppm docker image new命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockercompose


class New(EndPoint):
    """创建一个docker-compose文件."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "dockercompose_name": {
                "type": "string",
                "title": "f",
                "description": "dockerfile名字",
                "default": "docker-compose.yml"
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
            "compose_version": {
                "type": "string",
                "title": "w",
                "description": "docker-compose版本",
                "enum": ["2.4", "3.7", "3.8"]
            },
            "use_host_network": {
                "type": "boolean",
                "title": "u",
                "default": False
            },
            "language": {
                "description": "目标语言使用的dockerfile",
                "title": "l",
                "type": "string",
                "enum": ["py", "go"]
            },
            "extend": {
                "description": "是否使用c扩展",
                "title": "e",
                "type": "boolean",
                "default": False
            },
            "extra_hosts": {
                "type": "array",
                "description": "内部定义额外host:ip映射",
                "items": {
                    "type": "string"
                }
            },
            "fluentd_url": {
                "description": "使用fluentd收集log的url",
                "title": "d",
                "type": "string"
            },
            "nfs_addr": {
                "type": "string",
                "title": "n",
                "description": "nfs的地址"
            },
            "nfs_shared_path": {
                "type": "string",
                "description": "nfs共享的路径",
                "default": "/"
            },
            "use_nfs_v4": {
                "type": "boolean",
                "description": "",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "执行位置",
                "default": "."
            }
        }
    }


dockercompose_new = dockercompose.regist_sub(New)
