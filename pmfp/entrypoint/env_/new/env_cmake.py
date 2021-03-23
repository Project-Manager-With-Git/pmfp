"""初始化cpp的执行环境."""
import pkgutil
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.tools_info_utils import get_golang_version
from pmfp.utils.template_utils import template_2_content

CMakeLists_txt_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'CMakeLists.txt.temp')
if template_io:
    CMakeLists_txt_template = template_io.decode('utf-8')
else:
    raise AttributeError("go.mod模板失败")


def new_env_cmake(cwd: Path,
                  project_name: str,
                  version: str,
                  description: str,
                  language: Optional[str] = None) -> None:
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
        if language is None:
            language = "CXX"
        if language not in ("C", "CXX",):
            warnings.warn(f"CMake环境暂不支持语言{language}")
            return
        content = template_2_content(
            template=CMakeLists_txt_template,
            project_name=project_name,
            version=version,
            description=description,
            language=language)
        with open(cmake_env_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        bin_path = cwd.joinpath("bin")
        if bin_path.exists() and bin_path.is_dir():
            warnings.warn("bin目录已存在!")
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