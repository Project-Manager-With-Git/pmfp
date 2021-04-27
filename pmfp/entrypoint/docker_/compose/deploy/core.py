"""ppm docker compose deploy命令的处理."""
from typing import Dict
from schema_entry import EntryPoint
from ..core import dockercompose, common_schema_properties

properties: Dict[str, object] = {
    "dockercompose_name": {
        "type": "string",
        "title": "f",
        "description": "指定docker-compose文件名字",
    },
    "portainer_url": {
        "type": "string",
        "description": "指定部署去的portainer"
    },
    "portainer_username": {
        "type": "string",
        "description": "指定部署去的portainer的用户名"
    },
    "portainer_password": {
        "type": "string",
        "description": "指定部署去的portainer的密码"
    },
    "deploy_endpoint": {
        "type": "integer",
        "description": "指定部署去的portainer的节点位置"
    },
    "deploy_stack": {
        "type": "integer",
        "description": "指定部署去的portainer的stack位置,如果没有则创建,创建好后会将id号保存"
    },
    "stack_name": {
        "type": "string",
        "description": "指定部署的stack名"
    },
    "rebuild": {
        "type": "boolean",
        "description": "强制重新编译,只对local模式有效",
        "default": False
    },
    "update_version": {
        "type": "boolean",
        "description": "是否更新版本为当前项目版本",
        "default": False
    }
}

properties.update(common_schema_properties)


class Deploy(EntryPoint):
    """执行部署相关的工具.

    如果指定`portainer_url`则会尝试部署到portainer上,如果没有指定则尝试命令行部署.
    如果指定`dockercompose_name`则会使用找到的docker-compose更新,否则根据命令行创建compose更新.
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": properties
    }


dockercompose_deploy = dockercompose.regist_sub(Deploy)
