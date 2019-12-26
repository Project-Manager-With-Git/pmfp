"""项目文档创建,编译等,使用sphinx."""

import os
import http.server
import socketserver
import subprocess
from typing import Dict, Any, Optional
import chardet
from pmfp.utils import find_project_name_path
from pmfp.const import PROJECT_HOME


def _update_doc(config: Dict[str, Any]) -> Optional[bool]:
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
        print("更新python的docstring文档")
        if project_name_path.is_file():
            print("编译python的api文档")
            command = f"sphinx-apidoc -o document {project_name}.py"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode == 0:
                print(f"编译python的api文档完成!")
            else:
                print(f"编译python的api文档失败!")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))

        else:
            print("编译python的api文档")
            command = f"sphinx-apidoc -o document {project_name}"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode == 0:
                print(f"编译python的api文档完成!")
            else:
                print(f"编译python的api文档失败!")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
        print("更新python的docstring文档完成!")

    print("更新多语言翻译")
    command = "sphinx-build -b gettext document docs/locale"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode == 0:
        print(f"导入待翻译文本完成")
        command = "sphinx-intl update -p docs/locale -d document/locale"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"更新多语言翻译完成!")
        else:
            print(f"更新多语言翻译失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        print(f"导入待翻译文本失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))


def _build_doc(config: Dict[str, Any]) -> Optional[bool]:
    """编译项目文档.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    Returns:
        Optional[bool]: 未找到项目同名文件返回None,python项目正常编译返回True

    """
    print("编译文档")
    command = "sphinx-build -b html document docs"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"编译默认文档失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        command = "sphinx-build -D language=en -b html document docs/en"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print(f"编译文档英文文档失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            command = "sphinx-build -D language=zh -b html document docs/zh"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print(f"编译中文文档失败!")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("编译文档完成!")
        docs = PROJECT_HOME.joinpath("docs")
        nojekyll = docs.joinpath(".nojekyll")
        if not nojekyll.exists():
            with nojekyll.open("w", encoding="utf-8") as f:
                pass
    return True


def _serve_doc(config: Dict[str, Any]) -> bool:
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
        print(f"在端口`{PORT}`启动")
        httpd.serve_forever()
    return True


def _locale_doc(config: Dict[str, Any], locale: str):
    """doc命令.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    print("为文档新增小语种{locale}支持".format(locale=locale))
    command = "sphinx-intl update -p docs/locale -d document/locale -l {locale}".format(
        locale=locale)
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"新增小语种{locale}失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print(f"新增小语种{locale}成功")


def doc(config: Dict[str, Any], kwargs: Dict[str, Any]):
    """doc命令.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        kwargs (Dict[str, Any]): doc命令参数.
    """
    if kwargs["locale"]:
        _locale_doc(config, kwargs["locale"])
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
