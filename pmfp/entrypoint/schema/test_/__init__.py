"""检测json schema的example是否符合定义的模式schema."""
import json
import sys
from pathlib import Path
from typing import Optional
from pmfp.utils.url_utils import is_url, get_source_from_url
from pmfp.utils.schema_utils import is_validated
from .core import schema_test


@schema_test.as_main
def test_schema(file: str) -> None:
    """检查一个json schema文件中的例子是否符合自身的schema.

    Args:
        file (str): 模式文件地址

    """
    if is_url(file):
        schema_obj = json.loads(get_source_from_url(file))
    else:
        with open(file, "r", encoding='utf-8') as f:
            schema_obj = json.load(f)

    schema_examples = schema_obj.get("examples")
    if not schema_examples:
        print(f"模式定义文件 {file}没有列举例子")
        sys.exit(0)
    else:
        validated = True
        for example in schema_examples:
            if not is_validated(example, schema_obj):
                content = f"""not validated:
                {example}
                """
                validated = False
                print(content)
        if validated:
            print("schema is validated")
