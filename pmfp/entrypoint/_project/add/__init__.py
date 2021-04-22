"""ppm project add命令的处理."""
import warnings
import json
import shutil
from typing import Optional
from pmfp.utils.fs_utils import iter_dir_to_end, get_abs_path
from pmfp.utils.remote_cache_utils import ComponentTemplate
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from pmfp.utils.template_utils import template_2_content
from pmfp.entrypoint._project.info import InfoBase
from .core import project_add


@project_add.as_main
def add_component(component_string: str, located_path: Optional[str] = None, cwd: str = ".") -> None:
    """为项目添加组件.

    Args:
        component_string (str): 描述组件资源包的字符串,格式为"[{host}::]{repo_namespace}::{repo_name}[@{tag}]//{component_path}".
        located_path (Optional[str], optional): 放在本地的位置.
    """
    projctinfo = InfoBase()
    projctinfo([])
    projctinfo.config
    cwdp = get_abs_path(cwd)
    # 检查组件是否已经缓存
    cache_dir = get_cache_dir()
    componentpack = ComponentTemplate.from_component_string(component_string)
    sourcepackdir = componentpack.source_pack.source_pack_path(cache_dir)
    try:
        if componentpack.source_pack.tag == "latest":
            componentpack.source_pack.cache(cache_dir, throw=True)
        else:
            if not sourcepackdir.exists():
                componentpack.source_pack.cache(cache_dir, throw=True)
            else:
                if not sourcepackdir.is_dir():
                    warnings.warn(f"{sourcepackdir} 不是目录,请确认情况.")
                    return
    except Exception as e:
        print("检查组件是否已经缓存 失败")
        print(e)
        return
    print("检查组件是否已经缓存 完成")
    # 确保缓存后迁移到本项目后复制组件到项目
    pmfpconf = get_config_info()
    with open(sourcepackdir.joinpath(pmfpconf["template_config_name"]), encoding="utf-8") as f:
        sourcepack_config = json.load(f)
    sourcepack_language = sourcepack_config["language"]
    project_language = projctinfo.config.get("language")
    if project_language and sourcepack_language != project_language:
        warnings.warn(f"组件{component_string}语言{sourcepack_language}与项目语言{project_language}不匹配")
        return
    sourcepack_env = sourcepack_config.get("env")
    project_env = projctinfo.config.get("env")
    if project_env and sourcepack_env and sourcepack_env != project_env:
        warnings.warn(f"组件{component_string}执行环境{sourcepack_language}与项目执行环境{project_language}不匹配")
        return
    sourcepack_components = sourcepack_config["components"]
    target_component_info = sourcepack_components.get(componentpack.component_path)
    if not target_component_info:
        warnings.warn(f"组件{component_string}未被模板仓库注册")
        return
    target_component_path = sourcepackdir.joinpath(componentpack.component_path)
    if not target_component_path.exists():
        warnings.warn(f"组件{component_string}不存在")
        return
    if not located_path:
        default_path = target_component_info["default_path"]
        located_path = template_2_content(default_path, **projctinfo.config)
    target_located_path = cwdp.joinpath(located_path)
    if target_component_path.is_dir():
        if not target_located_path.exists():
            # target_located_path.mkdir(parents=True, exist_ok=False)
            shutil.copytree(target_component_path, target_located_path)
        else:
            warnings.warn(f"组件{component_string}的放置位置{target_located_path}已经存在")
            return
        # iter_dir_to_end(target_component_path, match=lambda x:)
    else:
        if not target_located_path.exists():
            # target_located_path.mkdir(parents=True, exist_ok=False)
            shutil.copyfile(target_component_path, target_located_path)
        else:
            warnings.warn(f"组件{component_string}的放置位置{target_located_path}已经存在")
            return

   