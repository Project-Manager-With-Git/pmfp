
# def query_grpc(url: str, protofile: str, method: str, payload: str, *,insecure:bool=False, plaintext: bool = False,format="json",cacert=None,cert=None,key=None) -> None:
#     """编译protobuffer为go语言模块.

#     Args:
#         files (List[str]): 待编译的protobuffer文件
#         includes (List[str]): 待编译的protobuffer文件所在的文件夹
#         to (str): 编译成的模块文件放到的路径
#         source_relative (bool): 是否使用路径作为包名,只针对go语言

#     """
#     command = "grpcurl -plaintext -d '{"value":"grpcurl"}' localhost:8888 proto.HelloService/Hello"
