"""清除资源包缓存."""
import re
import warnings
import shutil
from pathlib import Path
from typing import Optional, List
from pmfp.utils.fs_utils import remove_readonly
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from .core import cache_clean


def remove_by_mode(dirp: Path, mode: str = "except_latest") -> None:
    if mode == "except_latest":
        for p in dirp.iterdir():
            if p.is_dir():
                if p.name != "latest":
                    shutil.rmtree(p, onerror=remove_readonly)
                    print(f"{p} is removed")
            else:
                warnings.warn(f"{p} is not dir ... skip")
    elif mode == "only_hash":
        for p in dirp.iterdir():
            if p.is_dir():
                if re.match(r"^[a-f0-9]+$", p.name) and len(p.name) > 10:
                    shutil.rmtree(p, onerror=remove_readonly)
                    print(f"{p} is removed")
            else:
                warnings.warn(f"{p} is not dir ... skip")
    elif mode == "all":
        shutil.rmtree(dirp, onerror=remove_readonly)
        print(f"{dirp} is removed")
    else:
        raise AttributeError("unsupported mode")


@cache_clean.as_main
def sourcepack_clean(mode: str = "except_latest", host: Optional[str] = None,
                     repo_namespace: Optional[str] = None, repo_name: Optional[str] = None,
                     tags: Optional[List[str]] = None) -> None:
    """清除资源包的缓存."""
    cache_dir = get_cache_dir()
    if not cache_dir.is_dir():
        warnings.warn(f"{cache_dir} is not dir ... skip")
        return
    conf = get_config_info()
    # 删除单一项目
    if repo_name:
        if not host:
            host = conf["default_template_host"]
        if not repo_namespace:
            repo_namespace = conf["default_template_namespace"]
        if tags:
            for tag in tags:
                p = cache_dir.joinpath(f"{host}/{repo_namespace}/{repo_name}/{tag}")
                if p.is_dir():
                    shutil.rmtree(p, onerror=remove_readonly)
                    print(f"{p} is removed")
                else:
                    warnings.warn(f"{p} is not dir ... skip")
        else:
            p = cache_dir.joinpath(f"{host}/{repo_namespace}/{repo_name}")
            if p.is_dir():
                remove_by_mode(p, mode=mode)
            else:
                warnings.warn(f"{p} is not dir ... skip")
    else:
        # 删除全命名空间项目
        if repo_namespace:
            if not host:
                host = conf["default_template_host"]
            p = cache_dir.joinpath(f"{host}/{repo_namespace}")
            if p.is_dir():
                for pp in p.iterdir():
                    if pp.is_dir():
                        remove_by_mode(pp, mode=mode)
                    else:
                        warnings.warn(f"{pp} is not dir ... skip")
            else:
                warnings.warn(f"{p} is not dir ... skip")
        else:
            # 删除全host项目
            if host:
                p = cache_dir.joinpath(f"{host}")
                if p.is_dir():
                    for pp in p.iterdir():
                        if pp.is_dir():
                            for ppp in pp.iterdir():
                                if ppp.is_dir():
                                    remove_by_mode(ppp, mode=mode)
                                else:
                                    warnings.warn(f"{ppp} is not dir ... skip")
                        else:
                            warnings.warn(f"{pp} is not dir ... skip")
                else:
                    warnings.warn(f"{p} is not dir ... skip")
            else:
                # 删除全部项目
                for p in cache_dir.iterdir():
                    if p.is_dir():
                        for pp in p.iterdir():
                            if pp.is_dir():
                                for ppp in pp.iterdir():
                                    if ppp.is_dir():
                                        remove_by_mode(ppp, mode=mode)
                                    else:
                                        warnings.warn(f"{ppp} is not dir ... skip")
                            else:
                                warnings.warn(f"{pp} is not dir ... skip")
                    else:
                        warnings.warn(f"{p} is not dir ... skip")
