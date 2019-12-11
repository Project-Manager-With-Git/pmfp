"""执行python项目的build操作."""
import compileall
import shutil
import subprocess
import zipapp
from typing import (
    Dict,
    Any
)
from pathlib import Path
import chardet
from pmfp.const import PLATFORM, PROJECT_HOME
from pmfp.freeze import freeze
from pmfp.utils import find_project_name_path, get_python_path
from .utils import delete_source


def _delete_py_source(root_path: Path) -> None:
    """将python源码的.py文件删除.

    这是一个递归操作的函数.

    Args:
        p (Path): 要删除py文件的文件夹
    """
    delete_source(
        root_path,
        file_predication=lambda p: p.suffix == ".py" and p.name not in (
            "__main__.py", "__init__.py"),
        dir_predication=lambda p: p.name == "__pycache__"
    )


def _delete_c_source(root_path: Path) -> None:
    """将C语言的源码删除.

    删除的包括".c", ".cpp", ".oc"作为后缀的文件

    Args:
        p (Path): 要删除源文件的文件夹
    """
    delete_source(
        root_path,
        file_predication=lambda p: p.suffix in (".c", ".cpp", ".oc"),
        dir_iter_filter=lambda p: p.name != "src"
    )


def build_python_app(config: Dict[str, Any]) -> None:
    """将Application类型的python项目构造为可执行的.pyz文件.

    只会打包不是单文件的application项目

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json

    Raises:
        e: [description]

    """
    project_name = config["project-name"]
    print(f'编译打包python项目{project_name}为pyz文件')
    project_name_path = find_project_name_path(project_name)
    if find_project_name_path is False:
        print("找不到项目名同名目录")
        return
    else:
        if project_name_path.is_file():
            print("单文件python应用不用打包")
        else:
            setup = PROJECT_HOME.joinpath("setup.py")
            if "cython" in config["template"] and setup.exists():
                _build_cython_inplace(config)
            else:
                temp_path = PROJECT_HOME.joinpath("temp")
                try:
                    shutil.copytree(
                        str(project_name_path),
                        str(temp_path)
                    )
                    for p in temp_path.iterdir():
                        compileall.compile_dir(
                            str(p), force=True, legacy=True, optimize=2)
                        if p.is_dir():
                            _delete_py_source(p)
                    zipapp.create_archive(
                        temp_path,
                        target=project_name + ".pyz",
                        interpreter='/usr/bin/env python3'
                    )
                except Exception as e:
                    print(f"发生错误{type(e)}:{str(e)}")
                    raise e
                else:
                    print("完成编译打包python项目{project_name}为pyz文件!")
                finally:
                    if temp_path.exists():
                        shutil.rmtree(str(temp_path))


def _build_cython(config: Dict[str, Any], inplace: bool = False) -> None:
    """编译构建cython写的python项目.

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json
        inplace (bool, optional): Defaults to False. 用于区分是在源文件同目录下构建还是编译到build文件夹

    Raises:
        AttributeError: template中必须有cython字段才会编译
    """
    if not PROJECT_HOME.joinpath("requirements.txt").exists():
        print("没有requirements.txt,创建")
        freeze(config, {})
    project_name = config["project-name"]
    print(f'编译cython项目{project_name}到路径`build`')
    python_path = get_python_path(config)
    if "cython" in config["template"]:
        if inplace:
            command = f"{python_path} setup.py build_ext --inplace"
        else:
            command = f"{python_path} setup.py build"
        cc = config.get("gcc")
        if PLATFORM == 'Windows':
            if cc:
                command = command + f" -c {cc}"
            else:
                command = command + " -c msvc"
        else:
            if cc:
                command = f"CC={cc} " + command
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"完成编译cython项目!")
        else:
            print(f"编译cython项目失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))

        if inplace:
            _delete_c_source(PROJECT_HOME)
    else:
        raise AttributeError("template中必须有cython字段才会编译")


def _build_cython_inplace(config: Dict[str, Any]) -> None:
    """在cython源文件处构造模块.

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json
    """
    _build_cython(config, True)


def _build_curepython(config: Dict[str, Any]) -> None:
    """构造纯python项目的模块,到build文件夹下.

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json
    """
    if not PROJECT_HOME.joinpath("requirements.txt").exists():
        print("没有requirements.txt,创建")
        freeze(config,{})
    project_name = config["project-name"]
    print(f'编译纯python项目{project_name}到路径`build`')
    python_path = get_python_path(config)
    command = f"{python_path} setup.py build"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode == 0:
        print(f"完成build纯python项目!")
    else:
        print(f"build纯python项目失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))


def build_python_module(config: Dict[str, Any], inplace: bool) -> None:
    """构造python的模块.

    支持cython和纯python.

    Args:
        config (Dict[str, Any]): 项目的信息字典,来自pmfp.json
        inplace (bool): [description]
    """
    if "cython" in config["template"]:
        if inplace:
            _build_cython_inplace(config)
        else:
            _build_cython(config)
    else:
        _build_curepython(config)
