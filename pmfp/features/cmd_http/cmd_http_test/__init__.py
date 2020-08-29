"""编译protobuf的schema为不同语言的代码."""
import json
import yaml
from pmfp.utils.url_utils import http_query,is_url,get_source_from_url
from pmfp.utils.schema_utils import is_validated
from typing import Optional,Callable,NoReturn

def http_test(schema:str,serialization:str,url:str,method:str,*,
                auth:Optional[str]=None,
                auth_type:Optional[str]=None,
                payload:Optional[str]=None,
                payload_type:Optional[str]=None,
                stream:bool=False,
                verify:bool=False,
                cert:Optional[str]=None)->NoReturn:
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
        cb (Optional[Callable[[str],NoReturn]], optional): 获取到数据后的处理回调. Defaults to None.

    """
    if is_url(schema):
        schema_obj = json.loads(get_source_from_url(schema))
    else:
        with open(schema,"r", encoding='utf-8') as f:
            schema_obj = json.load(f)

    if serialization == "json":
        serialization_func = json.loads
    elif serialization == "yaml":
        serialization_func = yaml.loads
    else:
        raise AttributeError(f"不支持的序列化格式{serialization}")
    http_query(
        url=url,
        method=method,
        auth=auth, 
        auth_type=auth_type, 
        payload=payload, 
        payload_type=payload_type, 
        stream=stream, 
        verify=verify, 
        cert=cert, 
        cb=lambda x: print("validated") if is_validated(serialization_func(x),schema_obj) else print("not validated")
    )
