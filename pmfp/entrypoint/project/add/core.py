"""ppm test命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import project


class Add(EndPoint):
    """为项目添加组件."""

    argparse_noflag = "component_string"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["component_string"],
        "properties": {
            "component_string": {
                "type": "string",
                "description": "组件字符串指示资源位置,形式为`[{host}::]{repo_namespace}::{repo_name}[@{tag}]//{component_path}`"
            },
            "located_path": {
                "type": "string",
                "description": "放置位置,不设置则使用自带默认路径,可以使用jinja2模板"
            },
            "kv": {
                "type": "array",
                "description": "替换模板的默认参数,格式为`<key>::<value>`",
                "items": {
                    "type": "string"
                }
            },
            "cwd": {
                "type": "string",
                "description": "项目目录",
                "default": "."
            }
        }
    }


project_add = project.regist_sub(Add)
