import os
import zipapp
import shutil
import platform
import tempfile
import subprocess
import compileall
from pmfp.freeze import freeze
from pathlib import Path
from pmfp.const import (
    PROJECT_HOME,
    PLATFORM
)
from pmfp.utils import (
    find_project_name_path,
    get_python_path
)


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_py_source(p):
    if p.is_file():
        if p.suffix == ".py" and p.name not in ("__main__.py","__init__.py") :
            os.remove(str(p))
    else:
        if p.name == "__pycache__":
            try:
                shutil.rmtree(str(p), onerror=remove_readonly)
            except Exception as e:
                print(e)
        else:
            for i in p.iterdir():
                delete_py_source(i)
def delete_c_source(p):
    if p.is_file():
        if p.suffix in (".c",".cpp",".oc") :
            os.remove(str(p))
    else:
        for i in p.iterdir():
            if i.name != "src":
                delete_c_source(i)


def build_python_app(config):
    project_name = config["project-name"]
    print(f'build {project_name} to pyz file')
    project_name_path = find_project_name_path(project_name)
    if find_project_name_path is False:
        print("找不到项目名同名目录")
        return
    else:
        if project_name_path.is_file():
            print("单文件python应用不用打包")
        else:
            #temp = tempfile.mkdtemp(dir=".")
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
                        compileall.compile_dir(str(p), force=True, legacy=True, optimize=2)
                        if p.is_dir():
                            delete_py_source(p)
                    zipapp.create_archive(temp_path, target=project_name + ".pyz", interpreter='/usr/bin/env python3')
                except Exception as e:
                    print(f"发生错误{type(e)}:{str(e)}")
                    raise e
                finally:
                    if temp_path.exists():
                        shutil.rmtree(str(temp_path))

def _build_cython(config,inplace:bool=False):
    if not PROJECT_HOME.joinpath("requirements.txt").exists():
        print("没有requirements.txt,创建")
        freeze(config)
    project_name = config["project-name"]
    print(f'build {project_name} @ `build` ')
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
                command = f"CC={cc} "+command
        subprocess.check_call(command, shell=True)

        if inplace:
            delete_c_source(PROJECT_HOME)
    else:
        raise AttributeError("template中必须有cython字段才会编译")

def _build_cython_inplace(config):
    _build_cython(config,True)

def _build_curepython(config):
    if not PROJECT_HOME.joinpath("requirements.txt").exists():
        print("没有requirements.txt,创建")
        freeze(config)
    project_name = config["project-name"]
    print(f'build {project_name} @ `build` ')
    python_path = get_python_path(config)
    command = f"{python_path} setup.py build"
    subprocess.check_call(command, shell=True)

def build_python_module(config,inplace):
    if "cython" in config["template"]:
        if inplace:
            _build_cython_inplace(config)
        else:
            _build_cython(config)
    else:
        _build_curepython(config)
