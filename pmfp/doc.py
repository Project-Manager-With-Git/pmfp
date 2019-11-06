"""项目文档创建,编译等,使用sphinx."""

import os
import http.server
import socketserver
import subprocess
from typing import Dict, Any, Optional
from pmfp.utils import find_project_name_path
from pmfp.const import PROJECT_HOME

def _update_doc(config: Dict[str, Any])->Optional[bool]:
    """更新文档.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    Returns:
        Optional[bool]: 未找到项目同名文件返回None,python项目正常编译返回True

    """
    project_name = config["project-name"]
    project_name_path = find_project_name_path(project_name)
    if project_name_path is False:
        print("未找到项目名同名的文件或文件夹")
        return
    if config['project-language'] == "Python":
        print("update python docstring")
        if project_name_path.is_file():
            print("building apidoc")
            command = f"sphinx-apidoc -o document {project_name}.py"
            subprocess.check_call(command, shell=True)
            print("build apidoc done!")
        else:
            print("building apidoc")
            command = f"sphinx-apidoc -o document {project_name}"
            subprocess.check_call(command, shell=True)
            print("build apidoc done!")
        print("update python docstring done")

    print("update translation.")
    command = "sphinx-build -b gettext document docs/locale"
    subprocess.check_call(command, shell=True)
    command = "sphinx-intl update -p docs/locale -d document/locale"
    subprocess.check_call(command, shell=True)
    print("update translation done")

def _build_doc(config: Dict[str, Any])->Optional[bool]:
    """编译项目文档.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    Returns:
        Optional[bool]: 未找到项目同名文件返回None,python项目正常编译返回True

    """
    print("building document")
    command = "sphinx-build -b html document docs"
    subprocess.check_call(command, shell=True)
    command = "sphinx-build -D language=en -b html document docs/en"
    subprocess.check_call(command, shell=True)
    command = "sphinx-build -D language=zh -b html document docs/zh"
    subprocess.check_call(command, shell=True)
    print("build Document done!")
    docs = PROJECT_HOME.joinpath("docs")
    nojekyll = docs.joinpath(".nojekyll")
    if not nojekyll.exists():
        with nojekyll.open("w", encoding="utf-8") as f:
            pass
    return True

def _serve_doc(config: Dict[str, Any])->bool:
    """编译项目文档并在本地8000端口打开文档网页.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    Returns:
        [bool]: 正常展示返回True.

    """
    os.chdir("./docs")
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
    return True

def _locale_doc(config: Dict[str, Any],locale:str):
    """doc命令.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    print("new locale {locale} for document".format(locale=locale))
    command = "sphinx-intl update -p docs/locale -d document/locale -l {locale}".format(locale=locale)
    subprocess.check_call(command, shell=True)


def doc(config: Dict[str, Any], kwargs: Dict[str, Any]):
    """doc命令.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        kwargs (Dict[str, Any]): doc命令参数.
    """
    if kwargs["locale"]:
        _locale_doc(config,kwargs["locale"])
        return

    if kwargs["update"]:
        _update_doc(config)
        if kwargs["build"] or kwargs["serve"]:
            _build_doc(config)
            if kwargs["serve"]:
                _serve_doc(config)
    else:
        _build_doc(config)
        if kwargs["serve"]:
            _serve_doc(config)

