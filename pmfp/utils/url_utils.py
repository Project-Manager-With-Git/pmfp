"""与url字符串相关的工具代码."""
import json
from typing import Optional, Callable
from urllib.parse import urlparse
import requests as rq
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth1


def is_url(url: str) -> bool:
    """判断url是否是url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme])
    except ValueError:
        return False


def is_http_url(url: str) -> bool:
    """判断url是否是http请求的url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ("http", "https")
    except ValueError:
        return False


def is_file_url(url: str) -> bool:
    """判断url是否是文件协议相关的url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme]) and result.scheme == "file"
    except ValueError:
        return False


def query_http(url: str, method: str, *,
               auth: Optional[str] = None,
               auth_type: Optional[str] = None,
               payload: Optional[str] = None,
               payload_type: Optional[str] = None,
               stream: bool = False,
               verify: bool = False,
               cert: Optional[str] = None,
               cb: Optional[Callable[[str], None]] = None) -> None:
    """http请求并打印结果.

    Args:
        url (str): 要访问的http资源的地址
        method (str): 访问资源的方法
        auth (Optional[str], optional): 用户身份验证字符串. Defaults to None.
        auth_type (Optional[str], optional): 用户身份的验证类型. Defaults to None.
        payload (Optional[str], optional): 请求负载. Defaults to None.
        payload_type (Optional[str], optional): 请求的负载类型. Defaults to None.
        stream (bool, optional): 返回是否为流数据. Defaults to False.
        verify (bool, optional): https请求是否验证. Defaults to False.
        cert (Optional[str], optional): https请求的客户端认证文件. Defaults to None.
        cb (Optional[Callable[[str],None]], optional): 获取到数据后的处理回调. Defaults to None.

    """
    with rq.Session() as s:
        if verify:
            s.verify = verify
        if auth_type and auth:
            if auth_type == "basic":
                user, pwd = auth.split(",")
                s.auth = HTTPBasicAuth(user, pwd)
            if auth_type == "digest":
                user, pwd = auth.split(",")
                s.auth = HTTPDigestAuth(user, pwd)
            elif auth_type == "jwt":
                s.headers = rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + auth})
            elif auth_type == "oauth1":
                app_key, app_secret, oauth_token, oauth_token_secret = auth.split(",")
                s.auth = OAuth1(app_key, app_secret, oauth_token, oauth_token_secret)
            else:
                raise AttributeError(f"auth_type 参数 {auth_type} 目前不支持")
        if cert:
            cert_list = cert.split(",")
            cert_list_len = len(cert_list)
            if cert_list_len == 1:
                s.cert = cert_list[0]
            elif cert_list_len == 2:
                s.cert = (cert_list[0], cert_list[1])
            else:
                raise AttributeError(f"cert 参数 {cert} 不合法")

        if payload is None:
            if stream is True:
                with s.request(method.upper(), url, stream=True) as res:
                    for line in res.iter_lines(decode_unicode=True):
                        if line:
                            if cb:
                                cb(line)

            else:
                res = s.request(method.upper(), url)
                if cb:
                    cb(res.text)

        else:
            if payload_type == "stream":
                if stream is True:
                    with open(payload, "rb") as f:
                        with s.request(method.upper(), url, data=f, stream=True) as res:
                            for line in res.iter_lines(decode_unicode=True):
                                if line:
                                    if cb:
                                        cb(line)
                else:
                    with open(payload, "rb") as f:
                        res = s.request(method.upper(), url, data=f)
                        if cb:
                            cb(res.text)

            else:
                with open(payload, "r", encoding='utf-8') as fu:
                    payload_dict = json.load(fu)

                if stream is True:
                    if payload_type == "json":
                        with s.request(method.upper(), url, json=payload_dict, stream=True) as res:
                            for line in res.iter_lines(decode_unicode=True):
                                if line:
                                    if cb:
                                        cb(line)
                    elif payload_type == "form":
                        with s.request(method.upper(), url, data=payload_dict, stream=True) as res:
                            for line in res.iter_lines(decode_unicode=True):
                                if line:
                                    if cb:
                                        cb(line)
                    elif payload_type == "url":
                        with s.request(method.upper(), url, params=payload_dict, stream=True) as res:
                            for line in res.iter_lines(decode_unicode=True):
                                if line:
                                    if cb:
                                        cb(line)
                    else:
                        raise AttributeError(f"不支持的负载类型{payload_type}")
                else:
                    if payload_type == "json":
                        res = s.request(method.upper(), url, json=payload_dict)
                        if cb:
                            cb(res.text)
                    elif payload_type == "form":
                        res = s.request(method.upper(), url, data=payload_dict)
                        if cb:
                            cb(res.text)
                    elif payload_type == "url":
                        res = s.request(method.upper(), url, params=payload_dict)
                        if cb:
                            cb(res.text)
                    else:
                        raise AttributeError(f"不支持的负载类型{payload_type}")


def parse_file_url(url: str) -> str:
    """从file url中提取文件系统中的路径.

    Args:
        url (str): file url

    Returns:
        str: file url中提取出的路径

    """
    path_str = urlparse(url).path
    if ":" in path_str:
        path = path_str[1:]
    else:
        path = path_str
    return path


def parse_http_url(url: str) -> str:
    """从file url中提取文件系统中的路径.

    Args:
        url (str): file url

    Returns:
        str: file url中提取出的路径

    """
    path = urlparse(url).path

    return path


def get_source_from_url(url: str) -> str:
    """从指定url中回去源数据.

    注意只能获取静态http资源.

    Args:
        url (str): url地址

    Raises:
        AttributeError: url未成功返回
        AttributeError: 未支持的类型

    Returns:
        str: 内容文本

    """
    if is_http_url(url):
        rs = rq.get(url)
        if rs.status_code != 200:
            raise AttributeError(f"url {url} 未成功返回")
        else:
            return rs.text
    elif is_file_url(url):
        path = parse_file_url(url)
        with open(path, "r", encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        raise AttributeError(f"url {url} 未支持的类型")
