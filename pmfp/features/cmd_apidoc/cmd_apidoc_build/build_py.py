"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import default_succ_cb
from pmfp.utils.sphinx_utils import (
    sphinx_new,
    no_jekyll,
    sphinx_config,
    sphinx_build,
    sphinx_init_locale,
    sphinx_update_locale
)

def apidoc_build_py(code:str,output:str,source_dir:str,*,project_name:str,author:str, version:str) -> None:
    """为python项目构造api文档.

    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    def new_succ_cb(content:str)->None:
        default_succ_cb(content)
        print(f"在{source_dir}创建api文档源文件成功")
        append_content = """
import sphinx_rtd_theme
extensions += ['recommonmark', 'sphinx.ext.napoleon', 'sphinx.ext.mathjax','sphinx_rtd_theme']
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'logo_only': True,
    'navigation_depth': 5,
}
locale_dirs = ['locale/']   # path is example but recommended.
gettext_compact = False     # optional.

"""     
        sphinx_config(source_dir,append_content)
        print('完成初始化文档源文件')
        print("编译项目文档")
        sphinx_build(output=output,source_dir=source_dir,succ_cb=lambda x:no_jekyll(output))

    sphinx_new(code=code,source_dir=source_dir,project_name=project_name,author=author, version=version,
        succ_cb=new_succ_cb
    )