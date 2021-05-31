
"""请求指定grpc接口"""
import json
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run
from pmfp.utils.fs_utils import get_abs_path
from .core import grpc_query


@grpc_query.as_main
def query_grpc(url: str, service: str, method: str, payload: str, *,
               cwd: str = ".", plaintext: bool = False, insecure: bool = False,
               cacert: Optional[str] = None, cert: Optional[str] = None, key: Optional[str] = None) -> None:
    """请求grpc.

    Args:
        url (str): grpc的url
        service (str): 指定grpc提供的service使用 
        method (str): 要请求的方法
        payload (str): 请求的负载
        cwd (str, optional): 执行操作时的操作目录. Defaults to ".".
        plaintext (bool, optional): 是否不使用TLS加密传输. Defaults to False.
        insecure (bool, optional): 跳过服务器证书和域验证. Defaults to False.
        cacert (Optional[str], optional): 根证书位置. Defaults to None.
        cert (Optional[str], optional): 服务证书位置. Defaults to None.
        key (Optional[str], optional): 服务证书对应的私钥位置. Defaults to None.
    """
    pp = get_abs_path(payload, Path(cwd))
    with open(pp) as f:
        p = json.load(f)
    flags = " "
    if plaintext:
        flags += "-plaintext "
    if insecure:
        flags += "-insecure "
    if cert:
        flags += "-cert={cert} "
    if key:
        flags += "-key={key} "
    if cacert:
        flags += "-cacert={cacert} "
    c = json.dumps(p).replace('"', r'\"')
    command = f'grpcurl -d="{c}" {flags}{url} {service}/{method}'
    try:
        run(command, cwd=Path(cwd), visible=True)
    except Exception:
        warnings.warn("""执行query命令需要先安装grpcurl<https://github.com/fullstorydev/grpcurl/releases>""")
