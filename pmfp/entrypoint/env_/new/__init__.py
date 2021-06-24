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
from .env_py import init_py_env
from .env_cython import init_cython_env
from .env_go import init_go_env
from .env_c import init_c_env
from .env_cxx import init_cxx_env
from .env_js import init_js_env
from .env_md import init_md_env
from .core import env_new


readme_template = ""
changelog_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'readme.md.jinja')
if template_io:
    readme_template = template_io.decode('utf-8')
else:
    raise AttributeError("加载readme模板失败")

template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'changelog.md.jinja')
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


def freeze(env: str, language: str, *, cwd: Path,
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

    if env == "http":
        if version:
            content.update({"version": version})
        if author:
            content.update({"author": author})
        if author_email:
            content.update({"author_email": author_email})
        if keywords:
            content.update({"keywords": keywords})
        if description:
            content.update({"description": description})

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


def _new_nev(env: str, language: str, cwd: Path,
             project_name: str,
             version: str,
             author: str,
             author_email: str,
             description: str,
             keywords: str,
             requires: Optional[List[str]] = None,
             test_requires: Optional[List[str]] = None,
             setup_requires: Optional[List[str]] = None,
             extras_requires: Optional[List[str]] = None) -> None:
    if language == "py":
        init_py_env(env=env, cwd=cwd,
                    project_name=project_name,
                    version=version,
                    author=author,
                    author_email=author_email,
                    description=description,
                    keywords=keywords,
                    requires=requires,
                    test_requires=test_requires,
                    setup_requires=setup_requires,
                    extras_requires=extras_requires)
    elif language == "cython":
        init_cython_env(env=env, cwd=cwd,
                        project_name=project_name,
                        version=version,
                        author=author,
                        author_email=author_email,
                        description=description,
                        keywords=keywords,
                        requires=requires,
                        test_requires=test_requires,
                        setup_requires=setup_requires,
                        extras_requires=extras_requires)

    elif language == "go":
        init_go_env(cwd=cwd, project_name=project_name,
                    requires=requires,
                    test_requires=test_requires,
                    setup_requires=setup_requires,
                    extras_requires=extras_requires)
    elif language == "C":
        init_c_env(cwd=cwd, project_name=project_name, version=version, description=description)
    elif language == "CXX":
        init_cxx_env(cwd=cwd, project_name=project_name, version=version, description=description)
    elif language == "js":
        init_js_env(env=env, cwd=cwd, project_name=project_name, version=version, description=description, author=author,
                    author_email=author_email, keywords=keywords.split(", "), requires=requires, test_requires=test_requires)
    elif language == "md":
        init_md_env(cwd=cwd, project_name=project_name, description=description)
    else:
        print(f"暂不支持初始化{language}的环境")


def make_project_info_with_default(cwdp: Path, language: str,
                                   env: Optional[str] = None,
                                   project_name: Optional[str] = None,
                                   version: Optional[str] = None,
                                   author: Optional[str] = None,
                                   author_email: Optional[str] = None,
                                   description: Optional[str] = None,
                                   ) -> Dict[str, str]:
    result: Dict[str, str] = {"language": language}
    if not author:
        result["author"] = DEFAULT_AUTHOR
    else:
        result["author"] = author
    if not project_name:
        result["project_name"] = cwdp.resolve().name
    else:
        result["project_name"] = project_name
    if not version:
        result["version"] = "0.0.0"
    else:
        result["version"] = version
    if not author_email:
        result["author_email"] = ""
    else:
        result["author_email"] = author_email
    if not description:
        result["description"] = ""
    else:
        result["description"] = description
    if language == "py":
        if not env:
            result["env"] = "venv"
        else:
            if env not in ("venv", "conda", "pypy"):
                raise AttributeError(f"python 只支持环境`venv, conda, pypy`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "cython":
        if not env:
            result["env"] = "venv"
        else:
            if env not in ("venv", "conda",):
                raise AttributeError(f"cython 只支持环境`venv, conda`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "js":
        if not env:
            result["env"] = "node"
        else:
            if env not in ("node", "webpack",):
                raise AttributeError(f"js 只支持环境`node, webpack`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "go":
        if not env:
            result["env"] = "gomod"
        else:
            if env not in ("gomod", ):
                raise AttributeError(f"golang 只支持环境`gomod`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "CXX":
        if not env:
            result["env"] = "cmake"
        else:
            if env not in ("cmake", ):
                raise AttributeError(f"CXX 只支持环境`cmake`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "C":
        if not env:
            result["env"] = "cmake"
        else:
            if env not in ("cmake", ):
                raise AttributeError(f"C 只支持环境`cmake`,不支持环境`{env}`")
            else:
                result["env"] = env
    elif language == "md":
        if not env:
            result["env"] = "http"
        else:
            if env not in ("http", ):
                raise AttributeError(f"md 只支持环境`http`,不支持环境`{env}`")
            else:
                result["env"] = env
    return result


@ env_new.as_main
def new_env(language: str, *,
            env: Optional[str] = None,
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
        language (str): 目标项目使用的语言
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
        project_info_with_default = make_project_info_with_default(
            cwdp=cwdp,
            language=language,
            env=env,
            project_name=project_name,
            version=version,
            author=author,
            author_email=author_email,
            description=description)
        if not keywords:
            keywordstr = ""
        else:
            keywordstr = ", ".join(keywords)

        makereadme(
            cwd=cwdp,
            project_name=project_info_with_default["project_name"],
            author=project_info_with_default["author"],
            author_email=project_info_with_default["author_email"],
            description=project_info_with_default["description"],
            keywords=keywordstr
        )
        makechangelog(cwdp)
        _new_nev(
            env=project_info_with_default["env"],
            language=project_info_with_default["language"],
            cwd=cwdp,
            project_name=project_info_with_default["project_name"],
            version=project_info_with_default["version"],
            author=project_info_with_default["author"],
            author_email=project_info_with_default["author_email"],
            description=project_info_with_default["description"],
            keywords=keywordstr,
            requires=requires,
            test_requires=test_requires,
            setup_requires=setup_requires,
            extras_requires=extras_requires
        )
    except Exception as e:
        raise e
    else:
        freeze(env=project_info_with_default["env"],
               language=project_info_with_default["language"],
               project_name=project_info_with_default["project_name"],
               version=project_info_with_default["version"],
               author=project_info_with_default["author"],
               author_email=project_info_with_default["author_email"],
               description=project_info_with_default["description"],
               keywords=keywords,
               requires=requires,
               test_requires=test_requires,
               setup_requires=setup_requires,
               extras_requires=setup_requires,
               cwd=cwdp)
        print("执行环境序列化完成")
