import pkgutil
import warnings
from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path, path_to_str
from ..utils import (
    sphinx_new,
    no_jekyll,
    sphinx_config,
    sphinx_build,
    move_to_source,
    makeindex
)
from pmfp.utils.template_utils import template_2_content


AppendConfig = ""

source_io = pkgutil.get_data('pmfp.entrypoint.doc_.new.source_temp', 'pyappend_config.py.jinja')
if source_io:
    AppendConfig = source_io.decode('utf-8')
else:
    raise AttributeError("加载pyappend_config.py.jinja模板失败")

pyindexmd = ""

source_io = pkgutil.get_data('pmfp.entrypoint.doc_.new.source_temp', 'pyindex.md.jinja')
if source_io:
    pyindexmd = source_io.decode('utf-8')
else:
    raise AttributeError("加载pyindex.md.jinja模板失败")


def doc_new_py(code: str, output: str, source_dir: str, *, project_name: str, author: str, version: str, cwd: str = ".") -> None:
    """为python项目构造api文档.
    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
        cwd (str): 执行命令的根目录
    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")
    codep = get_abs_path(code, cwd=cwdp)
    codep_str = path_to_str(codep)
    outputp = get_abs_path(output, cwd=cwdp)
    source_dirp = get_abs_path(source_dir, cwd=cwdp)

    sphinx_new(source_dir=source_dirp, project_name=project_name, author=author, version=version, cwd=cwdp)
    try:
        appconfig = template_2_content(AppendConfig, code_path=codep_str)
        sphinx_config(source_dirp, appconfig)
        move_to_source(source_dir=source_dirp, root=cwdp)
        makeindex(source_dir=source_dirp, template=pyindexmd, project_name=project_name)
        sphinx_build(source_dir=source_dirp, doc_dir=outputp, cwd=cwdp)
        no_jekyll(outputp)
    except Exception as err:
        warnings.warn(f"""初始化python项目文档失败:

            {str(err)}

            构造python项目的api文档需要安装依赖:

            + pip install sphinx
            + pip install recommonmark
            + pip install sphinx-autoapi
            + pip install sphinx_rtd_theme
            """)
