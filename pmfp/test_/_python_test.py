"""测试python项目."""

import subprocess
from typing import Dict, Any, Sequence, Optional
from mypy import api
from pmfp.const import PROJECT_HOME, TYPECHECK_PATH
from pmfp.utils import (
    get_python_path,
    find_project_name_path
)


def _run_python_test(
        config: Dict[str, Any],
        html: bool,
        source: Optional[Sequence[str]])->None:
    """测试python代码.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        html (bool): 是否输出结果到html
        source (Sequence[str]): 是否要指定要测试的代码文件

    Raises:
        e: 测试失败会报错

    """
    print("unittest start")
    python_path = get_python_path(config)
    package_name = config["project-name"]
    if source:
        source = ",".join([package_name + "/" + i for i in source])
    else:
        source = package_name
    command = f"{python_path} -m coverage run --source={source} -m unittest discover -v -s ."
    try:
        subprocess.check_call(command, shell=True)
    except Exception as e:
        print("error")
        raise e
    else:
        if html:
            command = f"{python_path} -m coverage html -d covhtml"
            subprocess.check_call(command, shell=True)
        else:
            command = f"{python_path} -m coverage report"
            subprocess.check_call(command, shell=True)
    print("unittest done!")


def _run_python_typecheck(
        config: Dict[str, Any],
        html: bool,
        source: Optional[Sequence[str]]):
    """python类型检测.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        html (bool): 是否输出结果到html
        source (Sequence[str]): 是否要指定要测试的代码文件

    Raises:
        e: 测试失败会报错

    """
    print("type check start")
    language = config["project-language"]
    project_name = config["project-name"]
    project_name_path = find_project_name_path(project_name)
    if language == "Python":

        if project_name_path.is_file():
            package_name = [project_name + ".py"]
        else:
            package_name = [project_name]
            if source:
                package_name = []
                for i in PROJECT_HOME.joinpath(project_name).iterdir():
                    if i.stem in source:
                        package_name.append(f"{project_name}/{i.name}")
        if html:
            if not TYPECHECK_PATH.exists():
                TYPECHECK_PATH.mkdir()
            print(package_name)
            result = api.run(
                ["--no-site-packages","--ignore-missing-imports", '--html-report', TYPECHECK_PATH.name] + package_name
            )
        else:
            result = api.run(
                ["--no-site-packages","--ignore-missing-imports"] + package_name
            )
        if result[0]:
            print('\nType checking report:\n')
            print(result[0])  # stdout
        print("type check done!")
        return True
    else:
        print("only python can check type")
        return False


def run_python_test(
        config: Dict[str, Any],
        html: bool = False,
        typecheck: bool = False,
        source: Optional[Sequence[str]] = None)->None:
    """测试项目,支持python和node.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        html (bool): 是否输出结果到html
        typecheck (bool): 是做类型检测还是做单元测试.
        source (Sequence[str]): 是否要指定要测试的代码文件
    """
    if typecheck:
        _run_python_typecheck(config, html, source)
    else:
        _run_python_test(config, html, source)
