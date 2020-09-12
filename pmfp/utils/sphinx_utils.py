from pathlib import Path
from functools import partial
from pmfp.utils.run_command_utils import run_command,default_succ_cb
from typing import Optional,Callable


def sphinx_update_locale(output:str,source_dir:str,*,locales=["zh","en"],succ_cb:Optional[Callable[[str], None]] = None,fail_cb: Optional[Callable[[str], None]] = None):
    command = "sphinx-intl update -p {output}/locale -d {source_dir}/locale"
    for i in locales:
        command += f" -l {i}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)


def sphinx_init_locale(output:str,source_dir:str,*,succ_cb:Optional[Callable[[str], None]] = None,fail_cb: Optional[Callable[[str], None]] = None):
    command = f"sphinx-build -b gettext {source_dir} {output}/locale"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)

def sphinx_build(output:str,source_dir:str,*,succ_cb:Optional[Callable[[str], None]] = None,fail_cb: Optional[Callable[[str], None]] = None)->None:
    """执行sphinx的编译操作."""
    command = f"sphinx-build -b html {source_dir} {output}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)

def sphinx_config(source_dir:str,append_content:str)->None:
    """为sphinx的配置增加配置项.

    Args:
        source_dir (str): 文档源文件地址
        append_content (str): 要添加的配置文本.

    """
    with open(Path(source_dir).joinpath("conf.py"),"r",encoding="utf-8") as fr:
        content = fr.read()
    with open(Path(source_dir).joinpath("conf.py"),"w") as fw:
        new_content= content+append_content
        fw.write(new_content)

def no_jekyll(output:str):
    nojekyll = Path(output).joinpath(".nojekyll")
    if not nojekyll.exists():
        nojekyll.touch()

def sphinx_new(code:str,source_dir:str,project_name:str,author:str, version:str,*,succ_cb:Optional[Callable[[str], None]] = None,fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """为python项目构造api文档.

    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    command = f"sphinx-apidoc -F -H {project_name} -E -A {author} -V {version} -a -o {source_dir} {code}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)
