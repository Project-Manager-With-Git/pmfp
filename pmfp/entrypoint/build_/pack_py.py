"""打包py语言模块."""
import zipapp
import shutil
import compileall
import warnings
from typing import Optional, List
from pathlib import Path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_local_python
from pmfp.utils.fs_utils import get_abs_path, delete_source, path_to_str
from pmfp.utils.url_utils import is_http_url


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


def py_pack_lib(output_dir: Path, cwd: Path) -> None:
    python = get_local_python(cwd)
    output_dir_str = path_to_str(output_dir)
    command = f"{python} setup.py bdist_wheel --dist-dir={output_dir_str}"
    run(command, cwd=cwd, visible=True, fail_exit=True)


def py_pack_exec(code: str, project_name: str, *, output_dir: Path, cwd: Path, static: bool = False,
                 mini: bool = False, pypi_mirror: Optional[str] = None, requires: Optional[List[str]] = None) -> None:
    python = get_local_python(cwd)
    code_path = get_abs_path(code, cwd)
    temp_path = cwd.joinpath("temp_app")
    try:
        shutil.copytree(
            code_path,
            temp_path
        )
        if mini:
            for p in temp_path.iterdir():
                compileall.compile_dir(p, force=True, legacy=True, optimize=2)
                if p.is_dir():
                    _delete_py_source(p)
        if static and requires:
            for require in requires:
                if pypi_mirror and is_http_url(pypi_mirror):
                    command = f'{python} -m pip install -i {pypi_mirror} "{require}" --target temp_app'
                else:
                    command = f'{python} -m pip install "{require}" --target temp_app'
                run(command, cwd=cwd, visible=True, fail_exit=True)

        zipapp.create_archive(
            temp_path,
            target=output_dir.joinpath(f"{project_name}.pyz"),
            interpreter='/usr/bin/env python3'
        )
    except Exception as e:
        print(f"发生错误{type(e)}:{str(e)}")
        raise e
    else:
        print("完成编译打包python项目{project_name}为pyz文件!")

    finally:
        if temp_path.exists():
            shutil.rmtree(temp_path)


def py_pack(code: str, project_name: str, *,
            output_dir: Path,
            cwd: Path,
            pypi_mirror: Optional[str] = None,
            requires: Optional[List[str]] = None,
            build_as: str = "exec",
            static: bool = False,
            mini: bool = False,
            ) -> None:

    if build_as == "exec":
        py_pack_exec(code=code, project_name=project_name, output_dir=output_dir, cwd=cwd, pypi_mirror=pypi_mirror)
    elif "lib" in build_as:
        py_pack_lib(output_dir=output_dir, cwd=cwd)
    else:
        warnings.warn(f"python语言不支持打包类型{build_as}")
