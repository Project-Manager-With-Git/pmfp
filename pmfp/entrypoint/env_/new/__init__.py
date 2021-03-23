"""构造不同执行环境."""
import sys
import json
import pkgutil
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from pmfp.const import DEFAULT_AUTHOR, PMFP_CONFIG_DEFAULT_NAME
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.template_utils import template_2_content
from .env_py import (
    new_env_py_manifest,
    new_env_py_venv,
    new_env_py_conda,
    new_env_py_setup
)
from .env_go import new_env_go
from .env_cmake import new_env_cmake
from .core import env_new


readme_template = ""
changelog_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'readme.md.temp')
if template_io:
    readme_template = template_io.decode('utf-8')
else:
    raise AttributeError("加载readme模板失败")

template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'changelog.md.temp')
if template_io:
    changelog_template = template_io.decode('utf-8')
else:
    raise AttributeError("加载changelog模板失败")


def makereadme(cwd: Path, project_name: str,
               author: str,
               author_email: str,
               description: str,
               keywords: str) -> None:
    readmepath = cwd.joinpath("README.md")
    if readmepath.exists():
        warnings.warn("readme文件已经存在")
    else:
        readme = template_2_content(
            readme_template,
            project_name=project_name,
            author=author,
            author_email=author_email,
            description=description,
            keywords=keywords)
        with open(readmepath, "w", newline="", encoding="utf-8") as f:
            f.write(readme)
        print("根据模板创建README.md文件完成")


def makechangelog(cwd: Path) -> None:
    changelogpath = cwd.joinpath("CHANGELOG.md")
    if changelogpath.exists():
        warnings.warn("changelog文件已经存在")
    else:
        with open(changelogpath, "w", newline="", encoding="utf-8") as f:
            f.write(changelog_template)
        print("根据模板创建CHANGELOG.md文件完成")


def freeze(env: str, *, cwd: Path,
           project_name: Optional[str] = None,
           version: Optional[str] = None,
           author: Optional[str] = None,
           author_email: Optional[str] = None,
           description: Optional[str] = None,
           keywords: Optional[List[str]] = None,
           requires: Optional[List[str]] = None,
           test_requires: Optional[List[str]] = None,
           setup_requires: Optional[List[str]] = None,
           extras_requires: Optional[List[str]] = None,
           ) -> None:
    """将创建的环境信息保存到目录下的对应`pmfprc.json`中."""
    ppmrc = cwd.joinpath(PMFP_CONFIG_DEFAULT_NAME)
    content: Dict[str, Union[str, List[str]]] = {
        "env": env,
    }
    if env == "gomod":
        if version:
            content.update({"version": version})
        if author:
            content.update({"author": author})
        if author_email:
            content.update({"author_email": author_email})
        if description:
            content.update({"description": description})
        if keywords:
            content.update({"keywords": keywords})
        if requires:
            content.update({"requires": requires})
        if test_requires:
            content.update({"test_requires": test_requires})
        if setup_requires:
            content.update({"setup_requires": setup_requires})
        if extras_requires:
            content.update({"extras_requires": extras_requires})
    if env == "cmake":
        if author:
            content.update({"author": author})
        if author_email:
            content.update({"author_email": author_email})
        if keywords:
            content.update({"keywords": keywords})
        if requires:
            content.update({"requires": requires})
        if test_requires:
            content.update({"test_requires": test_requires})
        if setup_requires:
            content.update({"setup_requires": setup_requires})
        if extras_requires:
            content.update({"extras_requires": extras_requires})
    if ppmrc.exists():
        with open(ppmrc) as f:
            old = json.load(f)
        with open(ppmrc, "w", encoding="utf-8") as f:
            old.update(**content)
            json.dump(old, f, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        with open(ppmrc, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4, sort_keys=True)
    return None


def _new_nev(e: str, cwd: Path,
             project_name: str,
             version: str,
             author: str,
             author_email: str,
             description: str,
             keywords: str,
             language: Optional[str] = None,
             requires: Optional[List[str]] = None,
             test_requires: Optional[List[str]] = None,
             setup_requires: Optional[List[str]] = None,
             extras_requires: Optional[List[str]] = None) -> None:
    if e in ("venv", "conda"):
        if e == "conda":
            new_env_py_conda(cwd=cwd)
        else:
            new_env_py_venv(cwd=cwd)
        new_env_py_manifest(cwd=cwd, project_name=project_name)
        new_env_py_setup(cwd=cwd,
                         project_name=project_name,
                         version=version,
                         author=author,
                         author_email=author_email,
                         description=description,
                         keywords=keywords,
                         requires=requires,
                         test_requires=test_requires,
                         setup_requires=setup_requires,
                         extras_requires=extras_requires, cython=True if language == "cython" else False)
        print("构造python环境完成")

    elif e == "gomod":
        new_env_go(cwd=cwd, project_name=project_name)
    elif e == "cmake":
        new_env_cmake(cwd=cwd, project_name=project_name, version=version, description=description, language=language)
    else:
        print(f"暂不支持初始化环境{e}")


@ env_new.as_main
def new_env(env: str, *,
            language: Optional[str] = None,
            project_name: Optional[str] = None,
            version: Optional[str] = None,
            author: Optional[str] = None,
            author_email: Optional[str] = None,
            description: Optional[str] = None,
            keywords: Optional[List[str]] = None,
            requires: Optional[List[str]] = None,
            test_requires: Optional[List[str]] = None,
            setup_requires: Optional[List[str]] = None,
            extras_requires: Optional[List[str]] = None,
            cwd: str = ".") -> None:
    """构造不同执行环境.

    Args:
        env (str): 目标执行环境
        project_name (str): 项目名
        version (str): 项目版本
        author (str): 项目作者
        author_email (str, optional): 项目作者email. Defaults to "".
        description (str, optional): 项目简介. Defaults to "".
        keywords (Optional[List[str]], optional): 项目关键字. Defaults to None.
        cwd (str, optional): 命令执行根目录. Defaults to ".".
    """
    try:
        if cwd:
            cwdp = get_abs_path(cwd)
        else:
            cwdp = Path(".")
        if not author:
            author = DEFAULT_AUTHOR
        if not project_name:
            project_name = Path(cwd).resolve().name
        if not version:
            version = "0.0.0"
        if not author_email:
            author_email = ""
        if not description:
            description = ""
        if not keywords:
            keywordstr = ""
        else:
            keywordstr = ", ".join(keywords)

        makereadme(
            cwd=cwdp,
            project_name=project_name,
            author=author,
            author_email=author_email,
            description=description,
            keywords=keywordstr
        )
        makechangelog(cwdp)
        _new_nev(
            e=env,
            language=language,
            cwd=cwdp,
            project_name=project_name,
            version=version,
            author=author,
            author_email=author_email,
            description=description,
            keywords=keywordstr,
            requires=requires,
            test_requires=test_requires,
            setup_requires=setup_requires,
            extras_requires=extras_requires
        )
    except Exception as e:
        raise e
    else:
        freeze(env=env,
               project_name=project_name,
               version=version,
               author=author,
               author_email=author_email,
               description=description,
               keywords=keywords,
               requires=requires,
               test_requires=test_requires,
               setup_requires=setup_requires,
               extras_requires=setup_requires,
               cwd=cwdp)
        print("执行环境序列化完成")
