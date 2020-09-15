"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import default_succ_cb
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.sphinx_utils import (
    sphinx_update,
    sphinx_build,
    sphinx_update_locale,
    sphinx_new_locale,
    move_to_source
)


def apidoc_update_py(code: str, output: str, source_dir: str, *, root: str) -> None:
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

    def update_succ_cb(content: str) -> None:
        default_succ_cb(content)
        print('完成更新文档源文件')
        move_to_source(source_dir=source_dirp, root=rootp)

        def init_locale_succ_cb(coutent: str) -> None:
            default_succ_cb(coutent)
            print("更新多语言支持")

            def new_locale_succ_cb(coutent: str) -> None:
                default_succ_cb(coutent)
                print('导入多语言完成')
                sphinx_build(output=outputp, source_dir=source_dirp, cwd=rootp, locale="zh")

            sphinx_new_locale(output=outputp, source_dir=source_dirp, cwd=rootp, succ_cb=new_locale_succ_cb)

        sphinx_update_locale(output=outputp, source_dir=source_dirp, cwd=rootp, succ_cb=init_locale_succ_cb)

    sphinx_update(code=codep, source_dir=source_dirp, cwd=rootp,
                  succ_cb=update_succ_cb
                  )
