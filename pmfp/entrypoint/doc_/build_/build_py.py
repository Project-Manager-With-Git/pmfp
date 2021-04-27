import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.fs_utils import get_abs_path
from ..utils import (
    sphinx_build,
    move_to_source,
    sphinx_config_update_version
)


def doc_build_py(output: str, source_dir: str, *, version: Optional[str] = None, cwd: str = ".") -> None:
    """为python项目构造api文档.
    Args:
        output (str): html文档位置
        source_dir (str): 文档源码位置
        version (str): 项目版本
        cwd (str): 执行命令的根目录
    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")

    outputp = get_abs_path(output, cwd=cwdp)
    source_dirp = get_abs_path(source_dir, cwd=cwdp)
    if version:
        sphinx_config_update_version(source_dirp, version)
    move_to_source(source_dir=source_dirp, root=cwdp)
    try:
        sphinx_build(source_dir=source_dirp, doc_dir=outputp, cwd=cwdp)
    except Exception as err:
        warnings.warn(f"""编译python项目文档失败:

            {str(err)}

            构造python项目的api文档需要安装依赖:

            + pip install sphinx
            + pip install recommonmark
            + pip install sphinx-autoapi
            + pip install sphinx_rtd_theme
            """)
