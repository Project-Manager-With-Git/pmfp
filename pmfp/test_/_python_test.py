"""测试python项目."""

import subprocess
from typing import Dict, Any, Sequence, Optional
from mypy import api
import chardet
from pmfp.const import PROJECT_HOME, TYPECHECK_PATH
from pmfp.utils import (
    get_python_path,
    find_project_name_path
)


def _run_python_test(
        config: Dict[str, Any],
        html: bool,
        source: Optional[Sequence[str]]) -> None:
    """测试python代码.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        html (bool): 是否输出结果到html
        source (Sequence[str]): 是否要指定要测试的代码文件

    Raises:
        e: 测试失败会报错

    """
    print("开始单元测试")
    python_path = get_python_path(config)
    package_name = config["project-name"]
    if source:
        source = ",".join([package_name + "/" + i for i in source])
    else:
        source = package_name
    command = f"{python_path} -m coverage run --source={source} -m unittest discover -v -s ."
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("单元测试出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print("单元测试结果!")
        encoding = chardet.detect(res.stdout).get("encoding")
        print(res.stdout.decode(encoding))
        if html:
            command = f"{python_path} -m coverage html -d covhtml"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("生成覆盖率网页报告出错")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("生成覆盖率网页报告成功")
        else:
            command = f"{python_path} -m coverage report"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("生成覆盖率报告出错")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("生成覆盖率报告成功")
                encoding = chardet.detect(res.stdout).get("encoding")
                print(res.stdout.decode(encoding))
                print("单元测试完成!")


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
    print("类型检验开始")
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
                ["--no-site-packages", "--ignore-missing-imports",
                    '--html-report', TYPECHECK_PATH.name] + package_name
            )
        else:
            result = api.run(
                ["--no-site-packages", "--ignore-missing-imports"] + package_name
            )
        if result[0]:
            print('\n类型检验报告:\n')
            print(result[0])  # stdout
        print("类型检验结束!")
        return True
    else:
        print("只有python语言的项目有类型检验")
        return False


def run_python_test(
        config: Dict[str, Any],
        html: bool = False,
        typecheck: bool = False,
        source: Optional[Sequence[str]] = None) -> None:
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
