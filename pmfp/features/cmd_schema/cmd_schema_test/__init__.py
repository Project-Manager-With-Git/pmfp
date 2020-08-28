"""检测json schema的example是否符合定义的模式schema."""
import json
from pathlib import Path
from typing import NoReturn,Optional
from utils.url_utils import is_http_url,is_file_url,is_url

def _get_schema_from_http():


def test_schema(file:str) -> NoReturn:
    """检查一个json schema文件中的例子是否符合自身的schema.

    Args:
        file (str): 模式文件地址

    """
    if is_url(file):
        if is_file_url(file):
            pass
        elif is_http_url(file):
            pass
        else:

    else:

