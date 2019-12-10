"""为项目创建组件."""
import shutil
from typing import Dict, Any
from pathlib import Path
from pmfp.const import (
    PMFP_COMPONENTS_HOME,
    PROJECT_HOME,
    TEST_PATH,
    PMFP_TEST_TEMP
)

from .utils import iter_template_2_file, template_2_file
from ._new_test import python_test, js_test


def new_component(
        config: Dict[str, Any],
        path: str,
        to: str,
        rename: str,
        test: bool,
        **kwargs):
    """为项目新建一个组件.

    Args:
        config (Dict[str, Any]): 项目的配置字典
        path (str): 组件的位置
        to (str): 组件要复制到的位置
        rename (str): 组件要修改为什么名字
        test (bool): 是否要为组件添加测试

    """
    project_name = config.get("project-name") or "tempname"
    kws = {"project_name": project_name}
    if kwargs:
        kws.update(**kwargs)
    c_path = PMFP_COMPONENTS_HOME.joinpath(path)
    t_path = PROJECT_HOME.joinpath(to)
    if not c_path.exists():
        print(f"找不到对应的组件{str(c_path)}")
        return
    if not t_path.exists():
        print(f"找不到目标目录{str(t_path)},新建")
        t_path.mkdir(parents=True, exist_ok=False)

    if c_path.is_file():
        suname = c_path.stem
        suffixe = Path(suname).suffix
        to_path = t_path.joinpath(rename + suffixe)
        if to_path.exists():
            print(f"存在同名组件{rename}")
            return
        else:
            shutil.copy(
                str(c_path),
                str(to_path)
            )
            template_2_file(to_path, **kws)
    else:
        to_path = t_path.joinpath(rename)
        if t_path.joinpath(rename).exists():
            print(f"存在同名组件{rename}")
            return
        else:
            shutil.copytree(
                str(c_path),
                str(to_path)
            )
            iter_template_2_file(project_name, to_path)
    if test is True:
        if not PMFP_TEST_TEMP.joinpath(path).exists():
            print(f"未找到{path}对应的测试")
            return
        print("创建相应的测试组件")
        if TEST_PATH.exists():
            if TEST_PATH.is_file():
                print("test不是文件夹")
                return
        else:
            TEST_PATH.mkdir()
            print("创建测试文件夹")
        if config["project-language"] == "Python":
            python_test(project_name, rename, path)
        elif config["project-language"] == "Javascript":
            js_test(project_name, rename, path)
        else:
            print("语言不支持测试")
