"""编译go语言模块."""
import subprocess
import chardet


def build_pb_go(name: str, dir_: str, to: str, grpc: bool) -> None:
    """编译go语言模块.

    Args:
        name (str): 要编译的pb文件
        dir_ (str): 要编译的pb文件所在文件夹
        to (str): 将模块文件编译到目标位置
        grpc (bool): 编译grpc
    """
    if grpc:
        command = f"protoc -I {dir_} {dir_}/{name} --go_out=plugins=grpc:{to}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译grpc的protobuf项目<{name}>为go语言模块完成!")
        else:
            print(f"编译grpc的protobuf项目{name}为go语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        command = f"protoc -I={dir_} --go_out={to} {dir_}/{name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译protobuf项目<{name}>为go语言模块完成!")
        else:
            print(f"编译protobuf项目{name}为go语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
