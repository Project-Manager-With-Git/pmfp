"""清除资源包缓存."""
import shutil
from pathlib import Path
from pmfp.utils.fs_utils import get_cache_dir, remove_readonly
from .core import cache_clean


@cache_clean.as_main
def sourcepack_clean() -> None:
    """清除资源包的缓存."""
    cache_dir = get_cache_dir()
    for p in cache_dir.iterdir():
        try:
            shutil.rmtree(str(p), onerror=remove_readonly)
        except Exception as e:
            print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
