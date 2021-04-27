"""ppm cache list命令的处理."""
from pathlib import Path
from pmfp.utils.endpoint import EndPoint
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from .core import cache


class List(EndPoint):
    """获取当前基本环境信息."""
    verify_schema = False

    def do_main(self) -> None:
        cache_dir = get_cache_dir()
        print("[cache dir]:")
        print(cache_dir)
        conf = get_config_info()
        print("[cache list]:")
        for hostp in cache_dir.iterdir():
            if hostp.is_dir():
                for repo_namespacep in hostp.iterdir():
                    if repo_namespacep.is_dir():
                        for repo_namep in repo_namespacep.iterdir():
                            if repo_namep.is_dir():
                                tags = []
                                for tagp in repo_namep.iterdir():
                                    if tagp.is_dir():
                                        tags.append(tagp.name)
                                if hostp.name == conf["default_template_host"]:
                                    if repo_namespacep.name == conf["default_template_namespace"]:
                                        print(f"{repo_namep.name}@{tags}")
                                    else:
                                        print(f"{repo_namespacep.name}::{repo_namep.name}@{tags}")
                                else:
                                    print(f"{hostp.name}::{repo_namespacep.name}::{repo_namep.name}@{tags}")


cache_list = cache.regist_sub(List)
