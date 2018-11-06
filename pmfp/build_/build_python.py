import os
import zipapp
import shutil
import platform
import tempfile
import compileall
from pathlib import Path
from pmfp.const import PROJECT_HOME
from pmfp.utils import find_project_name_path


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_py_source(p):
    if p.is_file():
        if p.suffix == ".py" and p.name != "__main__.py":
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


def build_python_app(project_name):
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


def build_python_module(project_name):
    pass
