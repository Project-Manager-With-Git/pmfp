"""与url字符串相关的工具代码."""
from pathlib import Path
from urllib.parse import urlparse
import requests as rq

def is_url(url:str)->bool:
    """判断url是否是url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) 
    except ValueError:
        return False

def is_http_url(url)->bool:
    """判断url是否是http请求的url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ("http","https")
    except ValueError:
        return False

def is_file_url(url)->bool:
    """判断url是否是文件协议相关的url.

    Args:
        url (str): 待判断的url字符串

    Returns:
        bool: 是否是url

    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme == "file"
    except ValueError:
        return False

def get_source_from_url(url:str)->str:
    """从指定url中回去源数据.

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
        path_str = urlparse(url).path
        if ":" in path_str:
            path = path_str[1:]
        else:
            path = path_str
        with open(path,"r") as f:
            content = f.read()
        return content
    else:
        raise AttributeError(f"url {url} 未支持的类型")

