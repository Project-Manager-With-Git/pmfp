"""ppm docker compose命令的处理."""
from schema_entry import EntryPoint
from ..core import docker


class Compose(EntryPoint):
    """docker compose相关的工具."""


dockercompose = docker.regist_sub(Compose)


common_schema_properties = {
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
    "fluentd_url": {
        "description": "使用fluentd收集log的url,如果未定义则使用json-log",
        "type": "string"
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
    "command": {
        "type": "string",
        "description": "执行命令,可以是命令字符串,也可以是以`[]`包裹的命令列表形式"
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
    "add_envs": {
        "type": "array",
        "description": "添加环境变量,环境变量使用`<key>:<value>`的形式",
        "items": {
            "type": "string",
        }
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
    "add_networks": {
        "type": "array",
        "description": """添加网络
        <network_name>:添加内部网络
        <network_name>$$extra添加外部网络""",
        "items": {
            "type": "string",
        }
    },
    "add_volumes": {
        "type": "array",
        "description": """添加挂载,形式可以有3种
        <volume_name>::<path>;会在volumes种构造内部`volume_name`并挂载到服务的path目录
        <volume_name>$$extra::<path>;会在volumes种构造外部`volume_name`并挂载到服务的path目录
        <volume_name>$$path::<path>;直接挂载local路径到服务的path目录
        <volume_name>$$nfs@<nfs_addr>@<nfs_shared_path>@<nfs_opts>::<path>;挂载nfs到服务的path目录
        """,
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
