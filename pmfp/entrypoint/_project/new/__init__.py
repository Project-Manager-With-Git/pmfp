import json
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from pmfp.entrypoint.env_.new import new_env
from pmfp.entrypoint._project.add import new_env
from pmfp.utils.remote_cache_utils import SourcePack
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from .core import project_new


def check_and_cached(template_string: str, cache_dir: Path) -> Tuple[SourcePack, Path]:
    """检查组件的模板库是否有缓存,没有的话进行缓存.

    `latest`标签的模板库都会进行缓存更新.

    Args:
        template_string (str): 模板仓库字符串
        cache_dir (Path): 缓存根目录

    Raises:
        AttributeError: 组件缓存位置不是目录
        e: 其他执行中的异常

    Return:
        ComponentTemplate: 组件对象
    """
    source_pack = SourcePack.from_sourcepack_string(template_string)
    sourcepackdir = source_pack.source_pack_path(cache_dir)
    try:
        if source_pack.tag == "latest":
            source_pack.cache(cache_dir)
        else:
            if not sourcepackdir.exists():
                source_pack.cache(cache_dir, throw_clone=True)
            else:
                if not sourcepackdir.is_dir():
                    raise AttributeError(f"{sourcepackdir} 不是目录,请确认情况.")
    except Exception as e:
        raise e
    else:
        return source_pack, sourcepackdir


def check_source(pmfpconf: Dict[str, Any], env: str, sourcepackdir: Path, template_string: str, language: Optional[str] = None) -> Dict[str, Any]:
    """校验组件所在模板库的信息,通过的话返回模板库信息"""
    if not language:
        if env in ("venv", "conda"):
            language = "py"
        elif env == "gomod":
            language = "go"
        elif env == "cmake":
            language = "CXX"
        else:
            raise AttributeError(f"env {env} not support")
    with open(sourcepackdir.joinpath(pmfpconf["template_config_name"]), encoding="utf-8") as f:
        sourcepack_config = json.load(f)
    sourcepack_language = sourcepack_config["language"]
    if sourcepack_language != language:
        raise AttributeError(f"组件{template_string}语言{sourcepack_language}与项目语言{language}不匹配")
    sourcepack_env = sourcepack_config.get("env")
    if sourcepack_env and sourcepack_env != env:
        raise AttributeError(f"组件{template_string}执行环境{sourcepack_env}与项目执行环境{env}不匹配")
    return sourcepack_config


@project_new.as_main
def new_project(env: str, *,
                language: Optional[str] = None,
                project_name: Optional[str] = None,
                version: Optional[str] = None,
                author: Optional[str] = None,
                author_email: Optional[str] = None,
                description: Optional[str] = None,
                keywords: Optional[List[str]] = None,
                requires: Optional[List[str]] = None,
                template_string: Optional[str] = None,
                install: bool = False,
                cwd: str = ".") -> None:
    new_env(env=env,
            language=language,
            project_name=project_name,
            version=version,
            author=author,
            author_email=author_email,
            description=description,
            keywords=keywords,
            requires=requires,
            cwd=cwd)
    if template_string:
        pmfpconf = get_config_info()
        cache_dir = get_cache_dir()
        source_pack, sourcepackdir = check_and_cached(template_string, cache_dir)
        sourcepack_config = check_source(
            pmfpconf=pmfpconf,
            language=language,
            env=env,
            sourcepackdir=sourcepackdir,
            template_string=template_string)
        components = sourcepack_config.get("components")
        if components:
            cached_sourcepacks = []
            for component_name,component_info in components.items():
                _add_component(
                    cached_sourcepacks=cached_sourcepacks,
                    projectconfig=projectconfig,
                    pmfpconf=pmfpconf,
                    cache_dir=cache_dir,
                    component_string=component_string,
                    cwdp=cwdp,
                    located_path=located_path, kv=kv)
