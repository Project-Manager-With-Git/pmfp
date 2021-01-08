"""使用http请求获取资源."""
from typing import Optional
from pmfp.utils.url_utils import query_http
from .core import http_query


@http_query.as_main
def query(url: str, method: str, *,
          auth: Optional[str] = None,
          auth_type: Optional[str] = None,
          payload: Optional[str] = None,
          payload_type: Optional[str] = None,
          stream: bool = False,
          verify: bool = False,
          cert: Optional[str] = None) -> None:

    query_http(
        url=url,
        method=method,
        auth=auth,
        auth_type=auth_type,
        payload=payload,
        payload_type=payload_type,
        stream=stream,
        verify=verify,
        cert=cert, cb=print
    )
