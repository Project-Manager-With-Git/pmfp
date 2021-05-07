import pkgutil
import warnings
from pathlib import Path
from pmfp.const import GOLBAL_PYTHON_VERSION
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python, get_config_info
from pmfp.utils.template_utils import template_2_content
# python/cython公用
manifest_in_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'MANIFEST.in.jinja')
if template_io:
    manifest_in_template = template_io.decode('utf-8')
else:
    raise AttributeError("MANIFEST.in模板失败")


PipConfSource = ""
source_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'pip.conf.jinja')
if source_io:
    PipConfSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载pip.conf.jinja模板失败")


def new_env_py_venv(cwd: Path) -> None:
    """初始化python默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录

    """
    pmfp_conf = get_config_info()
    env_dir = pmfp_conf["python_local_env_dir"]
    env_path = cwd.joinpath(env_dir)
    if env_path.exists():
        warnings.warn("python的虚拟环境已存在!")
    else:
        python = get_global_python()
        command = f"{python} -m venv {env_dir}"
        run(command, cwd=cwd, visible=True, fail_exit=True)


def new_env_py_conda(cwd: Path) -> None:
    """初始化anaconda的python虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
    """
    pmfp_conf = get_config_info()
    env_dir = pmfp_conf["python_local_env_dir"]
    env_path = cwd.joinpath(env_dir)
    if env_path.exists():
        warnings.warn("python的虚拟环境已存在!")
    else:
        command = f"conda create -y -p {env_dir} python={GOLBAL_PYTHON_VERSION}"
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


def new_env_py_pypiconf(cwd: Path) -> None:
    """在项目下创建pip.conf文件.

    Args:
        cwd (Path): 项目根目录
    """
    pip_conf_path = cwd.joinpath("pip.conf")
    if pip_conf_path.exists():
        warnings.warn("pip.conf文件已经存在")
    else:
        content = PipConfSource
        with open(pip_conf_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        print("根据模板构造pip.conf文件成功")

# C/CXX公用


CMakeLists_txt_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'CMakeLists.txt.jinja')
if template_io:
    CMakeLists_txt_template = template_io.decode('utf-8')
else:
    raise AttributeError("go.mod模板失败")


def new_env_cmake(cwd: Path,
                  language: str,
                  project_name: str,
                  version: str,
                  description: str) -> None:
    """初始化C++默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
        project_name (str): 项目名
        version (str): 项目版本
        description: 项目说明
        language: 编程语言
    """

    cmake_env_path = cwd.joinpath("CMakeLists.txt")
    if cmake_env_path.exists():
        warnings.warn("CMakeLists.txt已存在!")
    else:
        content = template_2_content(
            template=CMakeLists_txt_template,
            project_name=project_name,
            version=version,
            description=description,
            language=language)
        with open(cmake_env_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        bin_path = cwd.joinpath("dist")
        if bin_path.exists() and bin_path.is_dir():
            warnings.warn("dist目录已存在!")
        else:
            bin_path.mkdir(parents=True)
        src_path = cwd.joinpath("src")
        if src_path.exists() and src_path.is_dir():
            warnings.warn("src目录已存在!")
        else:
            src_path.mkdir(parents=True)

        lib_path = cwd.joinpath("lib")
        if lib_path.exists() and lib_path.is_dir():
            warnings.warn("lib目录已存在!")
        else:
            lib_path.mkdir(parents=True)
        include_path = cwd.joinpath("include")
        if include_path.exists() and include_path.is_dir():
            warnings.warn("include目录已存在!")
        else:
            include_path.mkdir(parents=True)

        thirdpart_path = cwd.joinpath("thirdpart")
        if thirdpart_path.exists() and thirdpart_path.is_dir():
            warnings.warn("thirdpart目录已存在!")
        else:
            thirdpart_path.mkdir(parents=True)
