from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.sphinx_utils import (
    sphinx_new,
    no_jekyll,
    sphinx_config,
    sphinx_build,
    sphinx_update_locale,
    sphinx_new_locale,
    sphinx_index,
    move_to_source
)


def apidoc_new_py(code: str, output: str, source_dir: str, *, root: str, project_name: str, author: str, version: str) -> None:
    """为python项目构造api文档.
    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
    """
    if root:
        rootp = get_abs_path(root)
    else:
        rootp = Path(".")
    codep = get_abs_path(code, root=rootp)
    outputp = get_abs_path(output, root=rootp)
    source_dirp = get_abs_path(source_dir, root=rootp)

    def new_succ_cb(content: str) -> None:
        default_succ_cb(content)
        print(f"在{source_dir}创建api文档源文件成功")
        append_content = """
language = 'zh'
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
        sphinx_config(source_dirp, append_content)
        print('完成初始化文档源文件')
        move_to_source(source_dir=source_dirp, root=rootp)
        print("完成对readme和changelog的复制")
        sphinx_index(source_dir=source_dirp, project_name=project_name)
        print("完成重写入口模板")

        def build_succ_cb(coutent: str) -> None:
            default_succ_cb(coutent)
            no_jekyll(outputp)
            print('文档编译完成')

            def init_locale_succ_cb(coutent: str) -> None:
                default_succ_cb(coutent)
                print("初始化文档国际化完成")
                sphinx_new_locale(output=outputp, source_dir=source_dirp, cwd=rootp, locales=["zh", "en"])

            sphinx_update_locale(output=outputp, source_dir=source_dirp, cwd=rootp, succ_cb=init_locale_succ_cb)

        sphinx_build(output=outputp, source_dir=source_dirp, cwd=rootp, succ_cb=build_succ_cb)

    sphinx_new(code=codep, source_dir=source_dirp, project_name=project_name, author=author, version=version,
               cwd=rootp,
               succ_cb=new_succ_cb
               )
