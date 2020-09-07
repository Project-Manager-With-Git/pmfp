"""ppm cache命令的处理."""
from ..core import ppm, EntryPoint


ppm_cache = EntryPoint("cache")
ppm_cache.__doc__ = """ppm cache <subcommand>

    管理资源包缓存
    ppm cache 的子命令有:

    get                  获取资源包放入缓存
    clean                清除所有资源包缓存  
    """
ppm_cache.prog = "ppm cache"
ppm_cache.epilog = ''
ppm_cache.description = '管理资源包缓存'
ppm.regist_subcmd(ppm_cache)
