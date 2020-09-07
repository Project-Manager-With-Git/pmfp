from pathlib import Path
import shutil
from pmfp.utils.fs_utils import get_cache_dir,remove_readonly


def sourcepack_clean():
    cache_dir = get_cache_dir()
    for p in Path(cache_dir).iterdir():
        try:
            shutil.rmtree(str(p), onerror=remove_readonly)
        except Exception as e:
            print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
