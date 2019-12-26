"""展示组件的模块."""

from itertools import groupby
from pathlib import Path
from typing import Optional, List
from pmfp.const import PMFP_COMPONENTS_HOME
from ._find_path import find_path

EXCEPT = ["doc", "env", "readme", "setup", "test"]


def _find_all()->Optional[List[Path]]:
    """找到所有的组件."""
    def _find(path, depth):
        result = True if depth == 2 else False
        for i in EXCEPT:
            if "/" + i + "/" in str(path):
                result = False
        return result
    print("展示所有组件列表")
    result = find_path(PMFP_COMPONENTS_HOME, _find, max_depth=3)
    return result


def _find_all_language(language: str)->Optional[List[Path]]:
    """找到某一指定编程语言下的全部组件."""
    print(f"展示{language}的组件列表")
    p = PMFP_COMPONENTS_HOME.joinpath(language.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: depth == 1, max_depth=3)
    else:
        print(f"找不到{language}语言对应的组件")
        result = None
    return result


def _find_all_language_category(language: str, category: str)->Optional[List[Path]]:
    """找到某一指定编程语言下某一分类下的全部组件."""
    print(f"展示{language}中的{category}分类的组件列表")
    p = PMFP_COMPONENTS_HOME.joinpath(language.lower()).joinpath(category.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: depth == 0, max_depth=3)
    else:
        print(f"找不到{language}语言下{category}分类对应的组件")
        result = None
    return result


def _show_component_list(component_list: List[Path])->bool:
    """展示组件列表."""
    to_show = []
    for path in component_list:
        result = path.parts[-3:]
        to_show.append(result)
    gp_language = groupby(sorted(to_show, key=lambda x: x[0]), key=lambda x: x[0])
    for i, ite in gp_language:
        print(f"=====语言:{i}========")
        gp_c = groupby(sorted(ite, key=lambda x: x[1]), key=lambda x: x[1])
        for j, jte in gp_c:
            print(f"-----分类:{j}------")
            for k in jte:
                print(k[-2] + "-" + k[-1])
    return True


def _find_component_from_all(name: str)->Optional[List[Path]]:
    """从全部组件中找出某一名字的组件."""
    print(f"从全局查找组件{name}")
    result = find_path(
        PMFP_COMPONENTS_HOME,
        lambda path, depth: path.name == name and depth == 2,
        3
    )
    return result


def _find_component_from_language(name: str, language: str)->Optional[List[Path]]:
    """从某种语言的全部组件中找出某一名字的组件."""
    print(f"从{language}的组件中查找模板{name}")
    p = PMFP_COMPONENTS_HOME.joinpath(language.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: path.name == name and depth == 1, 3)
    else:
        print(f"{language}语言不存在")
        result = None
    return result


def _find_component_from_language_category(
        name: str,
        language: str,
        category: str)->Optional[List[Path]]:
    """从某种语言的某个分类中的全部组件中找出某一名字的组件."""
    print(f"从{language}的{category}模板中查找模板{name}")
    p = PMFP_COMPONENTS_HOME.joinpath(language.lower()).joinpath(category.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: path.name == name and depth == 0, 3)
    else:
        print(f"{language}语言的{category}分类不存在")
        result = None
    return result


def _show_component(language: Optional[str] = None, category: Optional[str] = None)->bool:
    """展示组件.

    Args:
        language (Optional[str], optional): Defaults to None. 组件使用的编程语言.
        category (Optional[str], optional): Defaults to None. 组件分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if language is None:
        component_list = _find_all()
    else:
        if category is None:
            component_list = _find_all_language(language)
        else:
            component_list = _find_all_language_category(language, category)
    if not component_list:
        print("未找到组件分类")
        result = False
    else:
        result = _show_component_list(component_list)
    return result


def _show_target_component(
        name: str,
        language: Optional[str] = None,
        category: Optional[str] = None)->bool:
    """展示组件.

    Args:
        name (Optional[str], optional): Defaults to None. 组件名.
        language (Optional[str], optional): Defaults to None. 组件使用的编程语言.
        category (Optional[str], optional): Defaults to None. 组件分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if language is None:
        component_list = _find_component_from_all(name)
    else:
        if category is None:
            component_list = _find_component_from_language(name, language)
        else:
            component_list = _find_component_from_language_category(name, language, category)
    if not component_list:
        print(f"找不到对应的组件{name}")
        result = False
    else:
        print(f"符合条件的组件有")
        result = _show_component_list(component_list)
    return result


def show(
        name: Optional[str] = None,
        language: Optional[str] = None,
        category: Optional[str] = None)->bool:
    """展示组件.

    Args:
        name (Optional[str], optional): Defaults to None. 组件名.
        language (Optional[str], optional): Defaults to None. 组件使用的编程语言.
        category (Optional[str], optional): Defaults to None. 组件分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if name is None:
        result = _show_component(language, category)
    else:
        result = _show_target_component(name, language, category)
    return result
