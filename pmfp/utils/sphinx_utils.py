from pathlib import Path
from functools import partial
from pmfp.utils.run_command_utils import run_command,default_succ_cb
from typing import Optional,Callable


def sphinx_new_locale(output:str,source_dir:str,*,
    locales=[],
    succ_cb:Optional[Callable[[str], None]] = None,
    fail_cb: Optional[Callable[[str], None]] = None)->None:
    """更新添加小语种支持.

    Args:
        output (str): 文档目录
        source_dir (str): 文档源文件位置
        locales (list, optional): 支持的语种. Defaults to ["zh","en"].
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.
    
    """
    command = f"sphinx-intl update -p {output}/locale -d {source_dir}/locale"
    for i in locales:
        command += f" -l {i}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)


def sphinx_update_locale(output:str,source_dir:str,*,
    succ_cb:Optional[Callable[[str], None]] = None,
    fail_cb: Optional[Callable[[str], None]] = None)->None:
    """初始化文档的小语种支持.

    Args:
        output (str): 文档目录
        source_dir (str): 文档源文件位置
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    command = f"sphinx-build -b gettext {source_dir} {output}/locale"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)

def sphinx_build(output:str,source_dir:str,*,
    locale:Optional[str] = None,
    succ_cb:Optional[Callable[[str], None]] = None,
    fail_cb: Optional[Callable[[str], None]] = None)->None:
    """执行sphinx的编译操作."""
    if locale:
        if locale == "zh":
            command = f"sphinx-build -D language={locale} -b html {source_dir} {output}"
        else:
            command = f"sphinx-build -D language={locale} -b html {source_dir} {output}/{locale}"

    else:
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
    """为目录添加一个空文件`.nojekyll`.

    Args:
        output (str): 放置的目录位置
        
    """
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
    command = f"sphinx-apidoc -F -E -H {project_name} -A {author} -V {version} -a -o {source_dir} {code}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)


def sphinx_update(code:str,source_dir:str, *,version:Optional[str],succ_cb:Optional[Callable[[str], None]] = None,fail_cb: Optional[Callable[[str], None]] = None) -> None:
    if version:
        command = f"sphinx-apidoc -V {version} -o {source_dir} {code}"
    else:
        command = f"sphinx-apidoc -o {source_dir} {code}"
    run_command(command,succ_cb=succ_cb,fail_cb=fail_cb)