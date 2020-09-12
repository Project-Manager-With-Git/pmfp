"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import default_succ_cb
from pmfp.utils.sphinx_utils import (
    sphinx_update,
    sphinx_build,
    sphinx_update_locale,
    sphinx_new_locale
)
from typing import Optional

def apidoc_update_py(code:str,output:str,source_dir:str,*,version:Optional[str]=None) -> None:
    """为python项目构造api文档.

    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    def update_succ_cb(content:str)->None:
        default_succ_cb(content)
        print('完成更新文档源文件')

        def init_locale_succ_cb(coutent:str)->None:
            default_succ_cb(coutent)
            print("更新多语言支持")

            def new_locale_succ_cb(coutent:str)->None:
                default_succ_cb(coutent)
                print('导入多语言完成')
                sphinx_build(output=output,source_dir=source_dir,locale="zh")

            sphinx_new_locale(output=output,source_dir=source_dir,succ_cb=new_locale_succ_cb)

        sphinx_update_locale(output=output,source_dir=source_dir,succ_cb=init_locale_succ_cb)

    sphinx_update(code=code,source_dir=source_dir,version=version,
        succ_cb=update_succ_cb
    )