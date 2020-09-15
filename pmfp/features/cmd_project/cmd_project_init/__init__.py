from pmfp.utils.remote_cache_utils import SourcePack
from pmfp.utils.fs_utils import get_cache_dir


def get_sourcepack(source_pack_string: str) -> None:
    sourcepack = SourcePack.from_sourcepack_string(source_pack_string)
    cache_dir = get_cache_dir()
    sourcepack.cache(cache_dir)
