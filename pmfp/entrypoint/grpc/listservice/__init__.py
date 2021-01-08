
"""列出远程grpc上的服务列表"""
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run_command
from .core import grpc_listservice


@grpc_listservice.as_main
def list_grpc(url: str, *,
              cwd: str = ".", plaintext: bool = False, insecure: bool = False,
              cacert: Optional[str] = None, cert: Optional[str] = None, key: Optional[str] = None) -> None:
    """列出grpc支持的服务.

    Args:
        url (str): grpc的url
        cwd (str, optional): 执行操作时的操作目录. Defaults to ".".
        plaintext (bool, optional): 是否不使用TLS加密传输. Defaults to False.
        insecure (bool, optional): 跳过服务器证书和域验证. Defaults to False.
        cacert (Optional[str], optional): . Defaults to None.
        cert (Optional[str], optional): [description]. Defaults to None.
        key (Optional[str], optional): [description]. Defaults to None.
    """
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
    command = f"grpcurl{flags}{url}"
    run_command(command, cwd == Path(cwd), visible=True).get()
