from schema_entry import EntryPoint
from ..core import schema


class Test(EntryPoint):
    """检查json schema文件."""
    argparse_noflag = "file"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["file"],
        "properties": {
            "file": {
                "type": "string",
                "description": "json schema文件.",
            }
        }
    }


schema_test = schema.regist_sub(Test)
