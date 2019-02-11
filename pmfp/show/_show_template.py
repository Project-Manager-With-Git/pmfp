"""查找显示项目模板."""
import json
from itertools import groupby
#from functools import partial
from collections.abc import Mapping
from pathlib import Path
from typing import Optional, List

from pmfp.const import PMFP_TEMPLATES_HOME
from ._find_path import find_path


def _find_all()->Optional[List[Path]]:
    """查找所有模板."""
    print("展示所有模板列表")
    result = find_path(
        PMFP_TEMPLATES_HOME,
        lambda path, depth: path.suffix == ".json" and path.is_file()
    )
    return result


def _find_all_language(language: str)->Optional[List[Path]]:
    """从指定语言中查找模板."""
    print(f"展示{language}的模板列表")
    p = PMFP_TEMPLATES_HOME.joinpath(language.lower())
    if p.is_dir():
        result = find_path(
            p,
            lambda path, depth: path.suffix == ".json" and path.is_file()
        )
    else:
        print(f"找不到{language}语言对应的模板")
        result = None
    return result


def _find_all_language_category(language: str, category: str)->Optional[List[Path]]:
    """从特定语言的特定类型中查找模板."""
    print(f"展示{language}中的{category}分类的模板列表")
    p = PMFP_TEMPLATES_HOME.joinpath(language.lower()).joinpath(category.lower())
    if p.is_dir():
        result = find_path(
            p,
            lambda path, depth: path.suffix == ".json" and path.is_file()
        )
    else:
        print(f"找不到{language}语言下{category}分类对应的模板")
        result = None
    return result


def _show_template_list(template_list: List[Path])->bool:
    """展示模板列表."""
    to_show = []
    for path in template_list:
        result = path.parts[-3:]
        to_show.append(result)
    gp_language = groupby(sorted(to_show, key=lambda x: x[0]), key=lambda x: x[0])
    ret = []
    for i, ite in gp_language:
        print(f"=====语言:{i}========")
        gp_c = groupby(sorted(ite, key=lambda x: x[1]), key=lambda x: x[1])
        for j, jte in gp_c:
            print(f"-----分类:{j}------")
            for k in jte:
                temp_name = k[-2] + "-" + k[-1].split(".")[0]
                print(temp_name)
                ret.append(temp_name)
    return ret


def find_template_detail(name: str, path: Path)->bool:
    """查找模板具体信息.

    Args:
        name (str): 模板名
        path (Path): 模板地址

    Returns:
        bool: 是否找到符合条件的模板

    """
    if path.suffix == ".json":
        with open(str(path), encoding="utf-8") as f:
            content = json.load(f)
        result = True if content["name"] == name else False
    else:
        result = False
    return result


def _find_module_from_all(name: str)->Optional[List[Path]]:
    """从全部模板中找出某一名字的模板."""
    print(f"从全局查找模板{name}")
    result = find_path(
        PMFP_TEMPLATES_HOME,
        lambda path, depth: find_template_detail(name, path)
    )
    return result


def _find_module_from_language(name: str, language: str)->Optional[List[Path]]:
    """从某种语言的全部模板中找出某一名字的模板."""
    print(f"从{language}的组件中查找模板{name}")
    p = PMFP_TEMPLATES_HOME.joinpath(language.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: find_template_detail(name, path))
    else:
        print(f"{language}语言不存在")
        result = None
    return result


def _find_module_from_language_category(
        name: str,
        language: str,
        category: str)->Optional[List[Path]]:
    """从某种语言的某个分类中的全部模板中找出某一名字的模板."""
    print(f"从{language}的{category}模板中查找模板{name}")
    p = PMFP_TEMPLATES_HOME.joinpath(language.lower()).joinpath(category.lower())
    if p.is_dir():
        result = find_path(p, lambda path, depth: find_template_detail(name, path))
    else:
        print(f"{language}语言的{category}分类不存在")
        result = None
    return result


def _show_template_list_detail(template_list: List[Path])->bool:
    """展示模板列表及各个模板细节."""
    for path in template_list:
        parts = "/".join(path.parts[-3:])
        with open(str(path), encoding="utf-8") as f:
            content = json.load(f)
        print(f"-----{parts}---------------------")
        for k, v in content.items():
            print(f"{k}:")
            if isinstance(v, Mapping):
                for i, j in v.items():
                    print(f'- {i}: {j}')
            else:
                print(f'- {v}')
    return True


def _show_template(
        language: Optional[str] = None,
        category: Optional[str] = None)->bool:
    """查找并展示模板列表.

    Args:
        language (Optional[str], optional): Defaults to None. 模板使用的语言.
        category (Optional[str], optional): Defaults to None. 模板的分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if language is None:
        template_list = _find_all()
    else:
        if category is None:
            template_list = _find_all_language(language)
        else:
            template_list = _find_all_language_category(language, category)
    if not template_list:
        print("空的模板分类")
        result = False
    else:
        result = _show_template_list(template_list)
    return result


def _show_target_template(
        name: str,
        language: Optional[str] = None,
        category: Optional[str] = None)->bool:
    """查找并展示模板列表.

    Args:
        name (str):模板的名字.
        language (Optional[str], optional): Defaults to None. 模板使用的语言.
        category (Optional[str], optional): Defaults to None. 模板的分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if language is None:
        template_list = _find_module_from_all(name)
    else:
        if category is None:
            template_list = _find_module_from_language(name, language)
        else:
            template_list = _find_module_from_language_category(name, language, category)
    if not template_list:
        print(f"找不到对应的模板{name}")
        result = False
    else:
        result = _show_template_list_detail(template_list)
    return result


def show(
        name: Optional[str] = None,
        language: Optional[str] = None,
        category: Optional[str] = None)->bool:
    """展示模板.

    Args:
        name (Optional[str], optional): Defaults to None. 模板的名字,如果有的话则会展示同名模板的详细信息.
        language (Optional[str], optional): Defaults to None. 模板使用的语言.
        category (Optional[str], optional): Defaults to None. 模板的分类.

    Returns:
        bool: 正确展示返回True,否则返回False.

    """
    if name is None:
        result = _show_template(language, category)
    else:
        result = _show_target_template(name, language, category)
    return result
