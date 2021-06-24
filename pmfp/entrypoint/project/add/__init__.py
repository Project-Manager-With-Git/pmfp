"""ppm project add命令的处理."""
import os
import warnings
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from pmfp.const import PMFP_CONFIG_DEFAULT_NAME
from pmfp.utils.fs_utils import iter_dir_to_end, get_abs_path
from pmfp.utils.remote_cache_utils import ComponentTemplate, SourcePack
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from pmfp.utils.template_utils import template_2_content
from pmfp.entrypoint.project.info import InfoBase
from .core import project_add


def sourcepack_check_and_cached(cached_sourcepack: List[str], source_pack: SourcePack, cache_dir: Path) -> Path:
    """检测资源包是否已经有缓存,没有就缓存.

    Args:
        cached_sourcepack (List[str]): 已经缓存过的资源包列表
        source_pack (SourcePack): 资源包对象
        cache_dir (Path): 缓存根目录

    Raises:
        AttributeError: 不是目录,请确认情况

    Returns:
        Path: 资源包的本地缓存路径
    """
    sourcepack_str = source_pack.as_sourcepack_string()
    sourcepackdir = source_pack.source_pack_path(cache_dir)
    if sourcepack_str in cached_sourcepack:
        return sourcepackdir
    else:
        try:
            if source_pack.tag == "latest":
                source_pack.cache(cache_dir, throw_clone=True)
            else:
                if not sourcepackdir.exists():
                    source_pack.cache(cache_dir, throw_clone=True)
                else:
                    if not sourcepackdir.is_dir():
                        raise AttributeError(f"{sourcepackdir} 不是目录,请确认情况.")
        except Exception as e:
            raise e
        else:
            cached_sourcepack.append(sourcepack_str)
            return sourcepackdir


def check_and_cached(cached_sourcepack: List[str], component_string: str, cache_dir: Path) -> Tuple[ComponentTemplate, Path]:
    """检查组件的模板库是否有缓存,没有的话进行缓存.

    `latest`标签的模板库都会进行缓存更新.

    Args:
        cached_sourcepack (List[str]): 已经缓存过的资源包列表
        component_string (str): 组件字符串
        cache_dir (Path): 缓存根目录

    Raises:
        AttributeError: 组件缓存位置不是目录
        e: 其他执行中的异常

    Return:
        ComponentTemplate: 组件对象
    """

    componentpack = ComponentTemplate.from_component_string(component_string)
    source_pack = componentpack.source_pack
    sourcepackdir = sourcepack_check_and_cached(
        cached_sourcepack=cached_sourcepack,
        source_pack=source_pack,
        cache_dir=cache_dir)
    return componentpack, sourcepackdir


def make_template_kv(sourcepack_config: Dict[str, Any], projectconfig: Dict[str, Any], kv: Optional[List[str]] = None, oldtemplate_kw: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """构造模板中匹配的kv.

    Args:
        kv (Optional[List[str]], optional): 外部输入的kv对. Defaults to None.

    Returns:
        Dict[str, str]: 模板render时的输入
    """
    sourcepack_kws = sourcepack_config["template_keys"]
    kvs = {}
    if kv:
        for i in kv:
            try:
                k, v = i.split("::")
            except Exception:
                warnings.warn(f"kv {kv} 解析错误,跳过")
                continue
            else:
                kvs[k] = v
    tempkv = {}
    tempkv.update(projectconfig)
    for key, info in sourcepack_kws.items():
        if oldtemplate_kw and oldtemplate_kw.get(key):
            tempkv[key] = oldtemplate_kw.get(key)
        else:
            if kvs.get(key):
                t = kvs[key]
            else:
                if info.get("ask"):
                    t = input(f"set {key} as:")
                    if not t:
                        t = info["default"]
                else:
                    t = info["default"]
            tempkv[key] = template_2_content(t, **projectconfig)
    return tempkv


def check_source(pmfpconf: Dict[str, Any], projectconfig: Dict[str, Any], sourcepackdir: Path, component_string: str) -> Dict[str, Any]:
    """校验组件所在模板库的信息,通过的话返回模板库信息"""
    with open(sourcepackdir.joinpath(pmfpconf["template_config_name"]), encoding="utf-8") as f:
        sourcepack_config = json.load(f)
    sourcepack_language = sourcepack_config.get("language")
    project_language = projectconfig.get("language")
    if sourcepack_language and project_language and sourcepack_language != project_language:
        raise AttributeError(f"组件{component_string}语言{sourcepack_language}与项目语言{project_language}不匹配")
    sourcepack_env = sourcepack_config.get("env")
    project_env = projectconfig.get("env")
    if project_env and sourcepack_env and sourcepack_env != project_env:
        raise AttributeError(f"组件{component_string}执行环境{sourcepack_env}与项目执行环境{project_env}不匹配")
    return sourcepack_config


def check_component(sourcepack_config: Dict[str, Any], componentpack: ComponentTemplate, component_string: str) -> Dict[str, Any]:
    """校验组件信息,通过的话返回组件信息."""
    sourcepack_components = sourcepack_config["components"]
    target_component_info = sourcepack_components.get(componentpack.component_path)
    if not target_component_info:
        raise AttributeError(f"组件{component_string}未被模板仓库注册")
    return target_component_info


def to_target_source(projectconfig: Dict[str, Any],
                     target_component_info: Dict[str, Any],
                     cwdp: Path,
                     sourcepackdir: Path,
                     target_source: str,
                     tempkv: Dict[str, Any],
                     located_path: Optional[str] = None,
                     root_default_path: Optional[str] = None) -> str:
    """将目标组件模板转换到项目目录."""
    def succ_callback(p: Path,) -> None:
        with open(p, encoding="utf-8") as f:
            content = template_2_content(f.read(), **tempkv)
        pp = p.with_name(p.stem)
        with open(pp, "w", encoding="utf-8", newline="") as fw:
            fw.write(content)
        os.remove(p)

    target_component_path = sourcepackdir.joinpath(target_source)
    if not target_component_path.exists():
        raise AttributeError(f"组件{ target_source }不存在")
    if not located_path:
        if root_default_path:
            located_path_t = root_default_path
        else:
            located_path_t = target_component_info["default_path"]
    else:
        located_path_t = located_path
    located_path_str = template_2_content(located_path_t, **tempkv)
    target_located_path = cwdp.joinpath(located_path_str)
    if target_component_path.is_dir():
        if not target_located_path.exists():
            shutil.copytree(target_component_path, target_located_path)
            iter_dir_to_end(target_located_path,
                            match=lambda p: p.suffix == ".jinja" and ".jinja" not in p.stem,
                            succ_cb=succ_callback)
        else:
            raise AttributeError(f"放置位置{target_located_path}已经存在")
    else:
        if not target_located_path.exists():
            if target_component_path.suffix == ".jinja":
                # 使用模板渲染成结果
                with open(target_component_path, encoding="utf-8") as f:
                    content = template_2_content(f.read(), **tempkv)
                if not target_located_path.parent.exists():
                    target_located_path.parent.mkdir(parents=True)
                with open(target_located_path, "w", encoding="utf-8", newline="") as fw:
                    fw.write(content)
            else:
                shutil.copyfile(target_component_path, target_located_path)
        else:
            raise AttributeError(f"放置位置{target_located_path}已经存在")
    return located_path_str


def save_to_components(cwdp: Path, component_string: str, located_path_str: str) -> None:
    """保存组件信息到项目配置."""
    if cwdp.joinpath(PMFP_CONFIG_DEFAULT_NAME).exists():
        with open(cwdp.joinpath(PMFP_CONFIG_DEFAULT_NAME), encoding='utf-8') as cf:
            c = json.load(cf)
    else:
        c = {}
    added_components = c.get("added_components", {})
    added_components[component_string] = located_path_str
    c.update(added_components=added_components)
    with open(cwdp.joinpath(PMFP_CONFIG_DEFAULT_NAME), "w", encoding='utf-8') as cfw:
        json.dump(c, cfw, indent=4)


def _add_component(cached_sourcepacks: List[str],
                   projectconfig: Dict[str, Any],
                   pmfpconf: Dict[str, Any],
                   cache_dir: Path,
                   component_string: str,
                   cwdp: Path, *,
                   located_path: Optional[str] = None,
                   save: bool = True,
                   kv: Optional[List[str]] = None,
                   root_default_path: Optional[str] = None,
                   oldtemplate_kw: Optional[Dict[str, Any]] = None) -> Tuple[ComponentTemplate, Dict[str, Any]]:
    componentpack, sourcepackdir = check_and_cached(
        cached_sourcepack=cached_sourcepacks,
        component_string=component_string,
        cache_dir=cache_dir
    )
    sourcepack_config = check_source(
        pmfpconf=pmfpconf,
        projectconfig=projectconfig,
        sourcepackdir=sourcepackdir,
        component_string=component_string
    )
    target_component_info = check_component(
        sourcepack_config=sourcepack_config,
        componentpack=componentpack,
        component_string=component_string
    )
    target_source = target_component_info["source"]
    tempkv = make_template_kv(
        sourcepack_config=sourcepack_config,
        projectconfig=projectconfig,
        kv=kv,
        oldtemplate_kw=oldtemplate_kw)
    if "//" in target_source:
        return _add_component(
            cached_sourcepacks=cached_sourcepacks,
            projectconfig=projectconfig,
            pmfpconf=pmfpconf,
            cache_dir=cache_dir,
            component_string=target_source,
            cwdp=cwdp,
            located_path=located_path,
            save=save,
            kv=kv,
            root_default_path=root_default_path,
            oldtemplate_kw=tempkv)
    else:
        located_path_str = to_target_source(projectconfig=projectconfig,
                                            target_component_info=target_component_info,
                                            cwdp=cwdp,
                                            sourcepackdir=sourcepackdir,
                                            target_source=target_source,
                                            tempkv=tempkv,
                                            located_path=located_path,
                                            root_default_path=root_default_path)
        if save:
            save_to_components(cwdp=cwdp, component_string=component_string, located_path_str=located_path_str)
        return componentpack, sourcepack_config


@project_add.as_main
def add_component(component_string: str, located_path: Optional[str] = None, kv: Optional[List[str]] = None, cwd: str = ".") -> None:
    """为项目添加组件.

    Args:
        component_string (str): 描述组件资源包的字符串,格式为"[{host}::]{repo_namespace}::{repo_name}[@{tag}]//{component_path}".
        located_path (Optional[str], optional): 放在本地的位置.
    """
    projectinfo = InfoBase()
    projectinfo([])
    projectconfig = projectinfo.config
    pmfpconf = get_config_info()
    cwdp = get_abs_path(cwd)
    cache_dir = get_cache_dir()
    cached_sourcepacks: List[str] = []
    componentpack, sourcepack_config = _add_component(
        cached_sourcepacks=cached_sourcepacks,
        projectconfig=projectconfig,
        pmfpconf=pmfpconf,
        cache_dir=cache_dir,
        component_string=component_string,
        cwdp=cwdp,
        located_path=located_path, kv=kv)
    sourcepack_config
