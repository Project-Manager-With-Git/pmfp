"""初始化python的执行环境."""
import pkgutil
import warnings
from pathlib import Path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.template_utils import template_2_content
from pmfp.const import GOLBAL_PYTHON_VERSION


manifest_in_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'MANIFEST.in.temp')
if template_io:
    manifest_in_template = template_io.decode('utf-8')
else:
    raise AttributeError("MANIFEST.in模板失败")

setup_py_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'setup.py.temp')
if template_io:
    setup_py_template = template_io.decode('utf-8')
else:
    raise AttributeError("setup.py模板失败")

setup_cfg_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'setup.cfg.temp')
if template_io:
    setup_cfg_template = template_io.decode('utf-8')
else:
    raise AttributeError("setup.cfg模板失败")


def new_env_py_venv(cwd: Path) -> None:
    """初始化python默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录

    """
    env_path = cwd.joinpath("env")
    if env_path.exists():
        warnings.warn("python的虚拟环境已存在!")
    else:
        python = get_global_python()
        command = f"{python} -m venv env"
        run(command, cwd=cwd, visible=True, fail_exit=True)


def new_env_py_conda(cwd: Path) -> None:
    """初始化anaconda的python虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
    """
    env_path = cwd.joinpath("env")
    if env_path.exists():
        warnings.warn("python的虚拟环境已存在!")
    else:
        command = f"conda create -y -p env python={GOLBAL_PYTHON_VERSION}"
        try:
            run(command, cwd=cwd, visible=True)
        except Exception:
            warnings.warn("初始化conda环境需要先安装anaconda或者miniconda")


def new_env_py_manifest(cwd: Path, project_name: str) -> None:
    """在项目下创建MANIFEST.in文件.

    Args:
        cwd (Path): 项目根目录
        project_name (str): 项目名
    """
    manifest_path = cwd.joinpath("MANIFEST.in")
    if manifest_path.exists():
        warnings.warn("MANIFEST.in文件已经存在")
    else:
        content = template_2_content(template=manifest_in_template, project_name=project_name)
        with open(manifest_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        print("根据模板构造MANIFEST.in文件成功")


def new_env_py_setup(cwd: Path, project_name: str,
                     version: str,
                     author: str,
                     author_email: str,
                     description: str,
                     keywords: str) -> None:
    """初始化python项目的setup.py和setup.cfg文件.

    Args:
        cwd (Path): [description]
    """
    setup_py_path = cwd.joinpath("setup.py")
    if setup_py_path.exists():
        warnings.warn("setup.py已存在!")
    else:
        content = template_2_content(template=setup_py_template)
        with open(setup_py_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        print("根据模板构造setup.py文件成功")

    setup_cfg_path = cwd.joinpath("setup.cfg")
    if setup_cfg_path.exists():
        warnings.warn("setup.cfg已存在!")
    else:
        content = template_2_content(
            template=setup_cfg_template,
            project_name=project_name,
            version=version,
            author=author,
            author_email=author_email,
            description=description,
            keywords=keywords
        )
        with open(setup_cfg_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        print("根据模板构造setup.cfg文件成功")
