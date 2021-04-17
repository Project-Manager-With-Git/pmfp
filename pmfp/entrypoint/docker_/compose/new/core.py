"""ppm docker image new命令的处理."""
from typing import Dict
from pmfp.utils.endpoint import EndPoint
from ..core import (
    dockercompose,
    common_schema_properties
)

properties: Dict[str, object] = {
    "dockerfile_dir": {
        "type": "string",
        "description": "dockerfile文件所在的文件夹,如果指定则会构造`build`段,在未指定`docker_register_namespace`时会被默认指定为`.`"
    },
    "dockerfile_name": {
        "type": "string",
        "description": "dockerfile文件名字,只有在dockerfile_dir有值时才会生效"
    },
    "updatemode": {
        "type": "string",
        "description": """当指定名称的compose已经存在时使用哪种方式更新,可以选择:
        `cover`:新的覆盖旧的,
        `level1`:以第一层为基准合并(services,volumes...),
        `level2`:以第二层为基准合并(level1基础上项目service单独更新)
        `level3`:以第二层为基准合并(service单独更新,并且尽量不动旧的)
        `level4`:以第三层为基准合并(level1基础上项目service单独更新,且service更新精细到内容一级)
        `level5`:以第三层为基准合并(service单独更新,且service更新精细到内容一级,并且尽量不动旧的)""",
        "enum": ["cover", "level1", "level2", "level3","level4", "level5"],
        "default": "merge_only_project"
    }
}

properties.update(common_schema_properties)


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
        "properties": properties
    }


dockercompose_new = dockercompose.regist_sub(New)
