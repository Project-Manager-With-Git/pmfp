"""ppm cache get命令的处理."""
from pmfp.utils.remote_cache_utils import SourcePack
from pmfp.utils.tools_info_utils import get_cache_dir
from .core import cache_get


@cache_get.as_main
def get_sourcepack(source_pack_string: str) -> None:
    """从远程指定位置获取资源包.

    Args:
        source_pack_string (str): 描述资源包的字符串,格式为"[{host}::]{repo_namespace}::{repo_name}[@{tag}]".

    """
    sourcepack = SourcePack.from_sourcepack_string(source_pack_string)
    cache_dir = get_cache_dir()
    sourcepack.cache(cache_dir)
