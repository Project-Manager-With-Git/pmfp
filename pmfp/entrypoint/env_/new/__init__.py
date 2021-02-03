"""构造不同执行环境."""
import sys
import json
import pkgutil
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.const import DEFAULT_AUTHOR
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.template_utils import template_2_content
from .env_py import (
    new_env_py_manifest,
    new_env_py_venv,
    new_env_py_conda,
    new_env_py_setup
)
from .env_go import new_env_go

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
        readmepath.write_text(readme, "utf-8")
        print("根据模板创建README.md文件完成")


def makechangelog(cwd: Path) -> None:
    changelogpath = cwd.joinpath("CHANGELOG.md")
    if changelogpath.exists():
        warnings.warn("changelog文件已经存在")
    else:
        changelogpath.write_text(changelog_template, "utf-8")
        print("根据模板创建CHANGELOG.md文件完成")


def freeze(env: List[str], *, cwd: Path,
           project_name: Optional[str] = None,
           version: Optional[str] = None,
           author: Optional[str] = None,
           author_email: Optional[str] = None,
           description: Optional[str] = None,
           keywords: Optional[List[str]] = None,
           ) -> None:
    """将创建的环境信息保存到目录下的`ppmrc.json`中."""
    ppmrc = cwd.joinpath("ppmrc.json")
    content = {
        "env": env,
    }
    if ppmrc.exists():
        with open(ppmrc) as f:
            old = json.load(f)
        with open(ppmrc, "w", encoding="utf-8") as f:
            old.update(**content)
            json.dump(old, f)
    else:
        with open(ppmrc, "w", encoding="utf-8") as f:
            json.dump(content, f)
    return None


def _new_nev(e: str, cwd: Path, project_name: str,
             version: str,
             author: str,
             author_email: str,
             description: str,
             keywords: str) -> None:
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
                         keywords=keywords)
        print(f"构造python环境完成")

    elif e == "gomod":
        new_env_go(cwd=cwd, project_name=project_name)
    else:
        print(f"暂不支持初始化环境{e}")


@env_new.as_main
def new_env(env: List[str], *,
            project_name: Optional[str] = None,
            version: Optional[str] = None,
            author: Optional[str] = None,
            author_email: Optional[str] = None,
            description: Optional[str] = None,
            keywords: Optional[List[str]] = None,
            cwd: str = ".") -> None:
    """构造不同执行环境.

    Args:
        env (List[str]): 目标执行环境
        project_name (str): 项目名
        version (str): 项目版本
        author (str): 项目作者
        author_email (str, optional): 项目作者email. Defaults to "".
        description (str, optional): 项目简介. Defaults to "".
        keywords (Optional[List[str]], optional): 项目关键字. Defaults to None.
        cwd (str, optional): 命令执行根目录. Defaults to ".".
    """
    try:
        envset = set(env)
        python_env = set(["conda", "venv"])
        if len(python_env & envset) >= 2:
            warnings.warn("python执行环境不能重复")
            sys.exit(1)
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
        for e in env:
            _new_nev(
                e=e,
                cwd=cwdp,
                project_name=project_name,
                version=version,
                author=author,
                author_email=author_email,
                description=description,
                keywords=keywordstr
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
               cwd=cwdp)
        print("执行环境序列化完成")
