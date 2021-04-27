"""查看远程grpc上的指定接口服务信息"""
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.run_command_utils import run
from .core import grpc_descservice


@grpc_descservice.as_main
def desc_grpc(url: str, service: str, *,
              cwd: str = ".", plaintext: bool = False, insecure: bool = False,
              cacert: Optional[str] = None, cert: Optional[str] = None, key: Optional[str] = None) -> None:
    """描述grpc支持的服务.

    Args:
        url (str): grpc的url
        service (str): 要查看的服务名
        cwd (str, optional): 执行操作时的操作目录. Defaults to ".".
        plaintext (bool, optional): 是否不使用TLS加密传输. Defaults to False.
        insecure (bool, optional): 跳过服务器证书和域验证. Defaults to False.
        cacert (Optional[str], optional): 根证书位置. Defaults to None.
        cert (Optional[str], optional): 服务证书位置. Defaults to None.
        key (Optional[str], optional): 服务证书对应的私钥位置. Defaults to None.
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
    command = f"grpcurl {flags}{url} describe {service}"
    try:
        run(command, cwd=Path(cwd), visible=True)
    except Exception:
        warnings.warn("""执行descservice命令需要先安装grpcurl<https://github.com/fullstorydev/grpcurl/releases>""")
