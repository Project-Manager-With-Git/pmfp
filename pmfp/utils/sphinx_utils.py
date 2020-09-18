"""sphinx构造api文档相关的公用组件."""
import shutil
from pathlib import Path
from typing import Optional, Callable, List
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.template_utils import template_2_content


def sphinx_new_locale(output: Path, source_dir: Path, *,
                      cwd: Optional[Path] = None,
                      locales: List[str] = [],
                      succ_cb: Optional[Callable[[str], None]] = None,
                      fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """更新添加小语种支持.

    Args:
        output (Path): 文档目录
        source_dir (Path): 文档源文件位置
        locales (List[str], optional): 支持的语种. Defaults to [].
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    command = f"sphinx-intl update -p {str(output)}/locale -d {str(source_dir.joinpath('locale'))}"
    for i in locales:
        command += f" -l {i}"
    run_command(command, cwd=cwd, succ_cb=succ_cb, fail_cb=fail_cb)


def sphinx_update_locale(output: Path, source_dir: Path, *,
                         cwd: Optional[Path] = None,
                         succ_cb: Optional[Callable[[str], None]] = None,
                         fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """初始化文档的小语种支持.

    Args:
        output (Path): 文档目录
        source_dir (Path): 文档源文件位置
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    command = f"sphinx-build -b gettext {str(source_dir)} {str(output.joinpath('locale'))}"
    run_command(command, cwd=cwd, succ_cb=succ_cb, fail_cb=fail_cb)


def sphinx_build(output: Path, source_dir: Path, *,
                 cwd: Optional[Path] = None,
                 locale: Optional[str] = None,
                 succ_cb: Optional[Callable[[str], None]] = None,
                 fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """执行sphinx的编译操作.

    Args:
        output (Path): 最终的文档文件夹位置.
        source_dir (Path): 文档资源文件夹位置.
        locale (Optional[str], optional): 要编译的小语种类型. Defaults to None.
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    if locale:
        if locale == "zh":
            command = f"sphinx-build -D language={locale} -b html {str(source_dir)} {str(output)}"
        else:
            command = f"sphinx-build -D language={locale} -b html {str(source_dir)} {output.joinpath(locale)}"

    else:
        command = f"sphinx-build -b html {str(source_dir)} {str(output)}"
    run_command(command, cwd=cwd, succ_cb=succ_cb, fail_cb=fail_cb)


def sphinx_config(source_dir: Path, append_content: str) -> None:
    """为sphinx的配置增加配置项.

    Args:
        source_dir (Path): 文档源文件地址
        append_content (str): 要添加的配置文本.

    """
    with open(source_dir.joinpath("conf.py"), "r", encoding="utf-8") as fr:
        content = fr.read()
    with open(source_dir.joinpath("conf.py"), "w", encoding="utf-8") as fw:
        new_content = content + append_content
        fw.write(new_content)


def sphinx_index(source_dir: Path, project_name: str) -> None:
    """为sphinx的配置增加配置项.

    Args:
        source_dir (Path): 文档源文件地址
        project_name (str): api文档服务的项目名.

    """
    template = """欢迎使用${project_name}!
======================================

.. toctree::
   :maxdepth: 1
   :caption: 使用指引:

   README

.. toctree::
   :maxdepth: 1
   :caption: 版本变更:

   Changelog

.. toctree::
   :maxdepth: 2
   :caption: 接口文档:

   ${project_name}

索引与搜索
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
    content = template_2_content(template, project_name=project_name.replace("-", "_"))
    with open(source_dir.joinpath("index.rst"), "w", encoding="utf-8") as wf:
        wf.write(content)


def no_jekyll(output: Path) -> None:
    """为目录添加一个空文件`.nojekyll`.

    Args:
        output (Path): 放置的目录位置

    """
    nojekyll = output.joinpath(".nojekyll")
    if not nojekyll.exists():
        nojekyll.touch()


def _move_to_source(source_dir: Path, file_name: str, *, root: Path) -> None:
    rootp = root.joinpath(file_name)
    sourcep = source_dir.joinpath(file_name)
    if rootp.is_file():
        shutil.copy(
            str(rootp),
            str(sourcep)
        )
        print(f"复制{file_name}成功")


def move_to_source(source_dir: Path, *, root: Path) -> None:
    """将项目根目录下的描述文件复制同步到项目下.

    Args:
        source_dir (Path): 文档源文件所在文件夹位置
        root (Path): 要移动文档的项目根目录.

    """
    _move_to_source(source_dir=source_dir, root=root, file_name="README.md")
    _move_to_source(source_dir=source_dir, root=root, file_name="CHANGELOG.md")


def sphinx_new(code: Path, source_dir: Path, project_name: str, author: str, version: str, *,
               cwd: Optional[Path] = None,
               succ_cb: Optional[Callable[[str], None]] = None,
               fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """为python项目构造api文档.

    Args:
        code (str): 项目源码位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    command = f"sphinx-apidoc -F -E -H {project_name} -A {author} -V {version} -a -o {str(source_dir)} {str(code)}"
    run_command(command, cwd=cwd, succ_cb=succ_cb, fail_cb=fail_cb)


def sphinx_update(code: Path, source_dir: Path, *,
                  cwd: Optional[Path] = None,
                  succ_cb: Optional[Callable[[str], None]] = None,
                  fail_cb: Optional[Callable[[str], None]] = None) -> None:
    """根据源码更新文档的源文件.

    Args:
        code (Path): 项目源码位置
        source_dir (Path): 文档源码位置
        succ_cb (Optional[Callable[[str], None]], optional): 成功的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[str], None]], optional): 失败的回调函数. Defaults to None.

    """
    command = f"sphinx-apidoc -o {str(source_dir)} {str(code)}"
    run_command(command, cwd=cwd, succ_cb=succ_cb, fail_cb=fail_cb)
