"""ppm cache命令的处理."""
from ..core import ppm, EntryPoint


ppm_cache = EntryPoint("cache")
ppm_cache.__doc__ = """ppm cache <subcommand>

    管理资源包缓存
    ppm cache 的子命令有:

    list                 创建一个protobuf文件
    build               编译protobuf到指定位置      
    """
ppm_cache.prog = "ppm proto"
ppm_cache.epilog = ''
ppm_cache.description = '管理protobuf文件的子命令'
ppm.regist_subcmd(ppm_cache)
