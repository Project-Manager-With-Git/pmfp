"""测试http请求的结果是否符合模式."""
import json
from typing import Optional, Callable, Any
import yaml
from pmfp.utils.url_utils import query_http, is_url, get_source_from_url
from pmfp.utils.schema_utils import is_validated
from .core import http_test


@http_test.as_main
def test_http(schema: str, serialization: str, url: str, method: str, *,
              auth: Optional[str] = None,
              auth_type: Optional[str] = None,
              payload: Optional[str] = None,
              payload_type: Optional[str] = None,
              stream: bool = False,
              verify: bool = False,
              cert: Optional[str] = None) -> None:
    """检测http请求的结果是否满足模式.

    Args:
        schema (str): 模式的地址,可以是url或者文件路径.
        serialization (str): 使用的序列化协议.
        url (str): 要访问的http资源的地址.
        method (str): 访问资源的方法.
        auth (Optional[str], optional): 用户身份验证字符串. Defaults to None.
        auth_type (Optional[str], optional): 用户身份的验证类型. Defaults to None.
        payload (Optional[str], optional): 请求负载. Defaults to None.
        payload_type (Optional[str], optional): 请求的负载类型. Defaults to None.
        stream (bool, optional): 返回是否为流数据. Defaults to False.
        verify (bool, optional): https请求是否验证. Defaults to False.
        cert (Optional[str], optional): https请求的客户端认证文件. Defaults to None.
        cb (Optional[Callable[[str],]], optional): 获取到数据后的处理回调. Defaults to None.

    """
    if is_url(schema):
        schema_obj = json.loads(get_source_from_url(schema))
    else:
        with open(schema, "r", encoding='utf-8') as f:
            schema_obj = json.load(f)
    serialization_func: Callable[[str], Any]
    if serialization == "json":
        serialization_func = json.loads
    elif serialization == "yaml":
        serialization_func = yaml.load
    else:
        raise AttributeError(f"不支持的序列化格式{serialization}")

    def _(x: str) -> None:
        if is_validated(serialization_func(x), schema_obj):
            print("validated")
        else:
            print("not validated")
    query_http(
        url=url,
        method=method,
        auth=auth,
        auth_type=auth_type,
        payload=payload,
        payload_type=payload_type,
        stream=stream,
        verify=verify,
        cert=cert,
        cb=_
    )
