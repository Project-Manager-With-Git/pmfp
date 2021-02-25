"""ppm docker image new命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import dockercompose


class New(EndPoint):
    """创建一个docker-compose文件.

    当指定的dockercompose文件存在时创建全新内容并覆盖原来老的compose文件,老的会被重新保存为`原名.{timestamp}_bak`;
    当指定的dockercompose文件不存在时创建新的compose文件.
    更新操作只能更新如下内容:

    1. service
    2. 外部networks声明
    3. 外部volumes声明
    4. 外部configs声明
    5. 外部secrits声明
    """
    argparse_noflag = "compose_version"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "compose_version": {
                "type": "string",
                "title": "w",
                "description": "指定生成的docker-compose版本",
                "enum": ["2.4", "3.7", "3.8"]
            },
            "dockercompose_name": {
                "type": "string",
                "title": "f",
                "description": "指定生成的docker-compose文件名字",
                "default": "docker-compose.yml"
            },
            "dockerfile_dir": {
                "type": "string",
                "description": "dockerfile文件所在的文件夹,如果指定则会构造`build`段,在未指定`docker_register_namespace`时会被默认指定为`.`"
            },
            "dockerfile_name": {
                "type": "string",
                "description": "dockerfile文件名字,只有在dockerfile_dir有值时才会生效"
            },
            "docker_register": {
                "type": "string",
                "title": "r",
                "description": "docker的镜像仓库位置"
            },
            "docker_register_namespace": {
                "type": "string",
                "title": "s",
                "description": "docker的镜像仓库中的命名空间,当与`project_name`都存在时会创建`image`段"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名,用于构造镜像名,当与`docker_register_namespace`都存在时会创建`image`段"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "镜像版本,用于构造镜像名"
            },
            "language": {
                "description": "目标语言使用的dockerfile,如果指定则会构造出`command`段",
                "title": "l",
                "type": "string",
                "enum": ["py", "go"]
            },
            "extend": {
                "description": "项目是否使用c扩展",
                "type": "boolean",
                "default": False
            },
            "use_host_network": {
                "type": "boolean",
                "title": "u",
                "description": "是否使用宿主机网络",
                "default": False
            },
            "ports": {
                "type": "array",
                "title": "p",
                "description": "开放端口,当已经设置`use_host_network`不会生效",
                "items": {
                    "type": "string"
                }
            },
            "extra_hosts": {
                "type": "array",
                "description": "内部定义额外host:ip映射",
                "items": {
                    "type": "string"
                }
            },
            "fluentd_url": {
                "description": "使用fluentd收集log的url,如果未定义则使用json-log",
                "type": "string"
            },
            "nfs_addr": {
                "type": "string",
                "description": "nfs的地址,有值时会设置`volumes`段并配置挂载nfs"
            },
            "nfs_shared_path": {
                "type": "string",
                "description": "nfs主机上的共享路径,只在nfs_addr设置时生效",
                "default": "/"
            },
            "use_nfs_v4": {
                "type": "boolean",
                "description": "是否使用nfsv4,只在nfs_addr设置时生效",
                "default": False
            },
            "add_service": {
                "type": "array",
                "title": "a",
                "description": "添加周边服务项",
                "items": {
                    "type": "string",
                    # "enmu": ["redis", "postgres", "zookeeper", "envoy"]
                }
            },
            "add_extra_networks": {
                "type": "array",
                "description": "添加外部网络",
                "items": {
                    "type": "string",
                }
            },
            "add_extra_volumes": {
                "type": "array",
                "description": "添加外部挂载",
                "items": {
                    "type": "string",
                }
            },
            "add_extra_configs": {
                "type": "array",
                "description": "添加外部配置文件",
                "items": {
                    "type": "string"
                }
            },
            "add_extra_secrets": {
                "type": "array",
                "description": "添加外部密钥",
                "items": {
                    "type": "string"
                }
            },
            "cwd": {
                "type": "string",
                "description": "执行位置",
                "default": "."
            },
        }
    }


dockercompose_new = dockercompose.regist_sub(New)
