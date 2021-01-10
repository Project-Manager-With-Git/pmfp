"""检测json schema的example是否符合定义的模式schema."""
import json
import sys
from pathlib import Path
from typing import Optional, Callable, IO, Any
import yaml
from pmfp.utils.url_utils import (
    is_url,
    is_http_url,
    is_file_url,
    parse_file_url,
    get_source_from_url
)
from pmfp.utils.schema_utils import is_validated
from pmfp.entrypoint.http.test_ import test_http
from .core import schema_check


@schema_check.as_main
def check_schema(schema: str, serialization: str, url: str, method: str, *,
                 auth: Optional[str] = None,
                 auth_type: Optional[str] = None,
                 payload: Optional[str] = None,
                 payload_type: Optional[str] = None,
                 stream: bool = False,
                 verify: bool = False,
                 cert: Optional[str] = None) -> None:
    """检测指定的数据是否满足模式.

    Args:
        schema (str): 模式的地址,可以是url或者文件路径.
        serialization (str): 使用的序列化协议.
        url (str): "请求的路径,可以是http/file的url或者文件系统的路径".
        method (str): 访问资源的方法.
        auth (Optional[str], optional): 用户身份验证字符串. Defaults to None.
        auth_type (Optional[str], optional): 用户身份的验证类型. Defaults to None.
        payload (Optional[str], optional): 请求负载. Defaults to None.
        payload_type (Optional[str], optional): 请求的负载类型. Defaults to None.
        stream (bool, optional): 返回是否为流数据. Defaults to False.
        verify (bool, optional): https请求是否验证. Defaults to False.
        cert (Optional[str], optional): https请求的客户端认证文件. Defaults to None.

    """
    if is_http_url(url):
        test_http(
            schema=schema,
            serialization=serialization,
            url=url,
            method=method,
            auth=auth,
            auth_type=auth_type,
            payload=payload,
            payload_type=payload_type,
            stream=stream,
            verify=verify,
            cert=cert
        )
    else:
        if is_file_url(url):
            path = parse_file_url(url)
        else:
            path = url
        serialization_func: Callable[[IO[str]], Any]
        if serialization == "json":
            serialization_func = json.load
        elif serialization == "yaml":
            serialization_func = yaml.load
        with open(path, "r", encoding='utf-8') as f:
            instance = serialization_func(f)
        if is_url(schema):
            schema_obj = json.loads(get_source_from_url(schema))
        else:
            with open(schema, "r", encoding='utf-8') as f:
                schema_obj = json.load(f)
        if is_validated(instance, schema_obj):
            print("validated")
        else:
            print("not validated")
