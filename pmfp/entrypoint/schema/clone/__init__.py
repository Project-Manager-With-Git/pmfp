"""克隆json schema模式文本."""
import os
import json
from pathlib import Path
from typing import Optional, Dict
from pmfp.utils.template_utils import jsontemplate_2_content
from pmfp.utils.url_utils import query_http, is_http_url, parse_http_url, is_file_url, parse_file_url
from pmfp.utils.fs_utils import get_abs_path


def clone_schema(url: str, method: str, out: str, *,
                 auth: Optional[str] = None,
                 auth_type: Optional[str] = None,
                 payload: Optional[str] = None,
                 payload_type: Optional[str] = None,
                 verify: bool = False,
                 cert: Optional[str] = None) -> None:
    """克隆一个json schema到本地文本.

    Args:
        name (str): 模式名
        path (str): 从根目录起的路径
        version (str): 模式版本
        root (str): 根目录.
        addr (str, optional): 网站域名.

    """
    def handdler(content: str) -> None:
        schema = json.loads(content)
        if "$schema" not in schema.keys():
            print("资源 {content} 不是 json schema 的模式文件")
        else:
            url = schema.get("$id")
            if is_http_url(url):
                p = parse_http_url(url)
            elif is_file_url(url):
                p = parse_file_url(url)
            else:
                print(f"未知的url形式 {url}")
                return
            name = Path(p).name
            out_p = get_abs_path(out)
            print("克隆到位置")
            with open(out_p.joinpath(name).as_posix(), "w") as f:
                json.dump(schema, f, ensure_ascii=False, indent=4, sort_keys=True)

    query_http(url, method,
               auth=auth,
               auth_type=auth_type,
               payload=payload,
               payload_type=payload_type,
               stream=False,
               verify=verify,
               cert=cert,
               cb=handdler)
