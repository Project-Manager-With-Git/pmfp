"""打包py语言模块."""
import shutil
import compileall
import warnings
from typing import Optional
from pathlib import Path
from pmfp.const import PLATFORM
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.tools_info_utils import get_local_python
from pmfp.utils.fs_utils import get_abs_path, delete_source


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
    python = get_local_python(cwd.joinpath("env"))
    if PLATFORM == 'Windows':
        output_dir_str = str(output_dir).replace("\\", "\\\\")
    else:
        output_dir_str = str(output_dir)
    command = f"{python} setup.py bdist_wheel --dist-dir={output_dir_str}"
    run_command(
        command, cwd=cwd
    ).catch(
        lambda err: warnings.warn(f"""打包为wheel失败
            {str(err)}
            """)
    ).get()


def py_pack_exec(code: str, project_name: str, *, output_dir: Path, cwd: Path, pypi_mirror: Optional[str] = None) -> None:
    python = get_local_python(cwd.joinpath("env"))
    if PLATFORM == 'Windows':
        output_dir_str = str(output_dir).replace("\\", "\\\\")
    else:
        output_dir_str = str(output_dir)

    code_path = get_abs_path(code, cwd)
    temp_path = cwd.joinpath("app")
    try:
        shutil.copytree(
            code_path,
            temp_path
        )
        for p in temp_path.iterdir():
            compileall.compile_dir(p, force=True, legacy=True, optimize=2)
            if p.is_dir():
                _delete_py_source(p)
        requirements_path = cwd.joinpath("requirements.txt")
        if requirements_path.exists():
            if pypi_mirror and is_http_url(pypi_mirror):
                command = f"{python} -m pip install -i {pypi_mirror}  -r requirements.txt --target app"
            else:
                command = f"{python} -m pip install  -r requirements.txt --target app"
            run_command(
                command, cwd=cwd
            ).catch(
                lambda err: warnings.warn(f"""为app安装依赖失败
                    {str(err)}
                    """)
            ).get()

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
            shutil.rmtree(temp_path)


def py_pack(code: str, project_name: str, *,
            output_dir: Path,
            cwd: Path,
            pypi_mirror: Optional[str] = None,
            build_as: str = "exec",
            ) -> None:

    if not cwd.joinpath("go.mod").exists():
        warnings.warn("go语言项目需要先有go.mod")
        return
    if build_as == "exec":
        py_pack_exec(code=code, project_name=project_name, output_dir=output_dir, cwd=cwd, pypi_mirror=pypi_mirror)
    elif:
        py_pack_lib(output_dir=output_dir, cwd=cwd)
    else:
        warnings.warn(f"python语言不支持打包类型{build_as}")

    command = "go build"
    output_dir_str = ""
    if PLATFORM == 'Windows':
        output_dir_str = str(output_dir).replace("\\", "\\\\")
    else:
        output_dir_str = str(output_dir)
    target_str = f"{output_dir_str}/{project_name}"
    command += f" -o {target_str} {code}"
    if for_linux_arch:
        env.update({
            "GOARCH": for_linux_arch,
            "GOOS": "linux"
        })
    run_command(
        command, cwd=cwd, env=env
    ).catch(
        lambda err: warnings.warn(f"""编译失败
            {str(err)}
            """)
    ).get()
