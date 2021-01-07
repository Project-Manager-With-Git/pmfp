"""启动一个简易的http静态服务器."""
import sys
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from typing import Dict, Any, List
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.fs_utils import get_global_python


def http_serv(port: int, root: str, bind: str) -> None:
    """启动http静态服务.

    Args:
        port (int): 端口
        root (str): 启动的根目录
        bind (str): 绑定的ip

    """
    ServerClass = ThreadingHTTPServer
    HandlerClass = partial(SimpleHTTPRequestHandler, directory=root)
    server_address = (bind, port)
    #protocol = "HTTP/1.0"
    #HandlerClass.protocol_version = protocol
    with ServerClass(server_address, HandlerClass) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
