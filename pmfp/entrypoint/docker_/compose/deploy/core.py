"""ppm test命令的处理."""
from typing import Dict
from schema_entry import EntryPoint
from ..core import dockercompose, common_schema_properties

properties: Dict[str, object] = {
    "portainer_url": {
        "type": "string",
        "description": "指定部署去的portainer",
    },
    "portainer_username": {
        "type": "string",
        "description": "指定部署去的portainer的用户名",
    },
    "portainer_password": {
        "type": "string",
        "description": "指定部署去的portainer的密码",
    },
    "deploy_path": {
        "type": "string",
        "description": """指定部署去的portainer的位置,
        其形式为`<ENDPOINT_ID>[/<STACK_ID>[/<SERVICE_NAME>;...]],<ENDPOINT_ID>[/<STACK_ID>[/<SERVICE_NAME>;...]]...`,
        如果不设置则不会部署,
        每一段中如果可以用`/`拆分为3段则表示替换,如果能拆分为2段则表示在已有stack中添加或者替换与项目名相同的service,如果只有一段表示新建一个stack
        """,
    }
}
properties.update(common_schema_properties)


class Deploy(EntryPoint):
    """执行部署相关的工具.

    如果指定`portainer_url`则会尝试部署到portainer上,如果没有指定则尝试命令行部署
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": properties
    }


dockercompose_deploy = dockercompose.regist_sub(Deploy)
