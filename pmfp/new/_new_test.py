"""各种语言的基本测试模板."""
import shutil
from pathlib import Path
from pmfp.const import (
    TEST_PATH,
    PMFP_TEST_TEMP
)
from .utils import iter_template_2_file


def python_test(project_name: str, rename: str, path: Path):
    """为python组件创建测试.

    Args:
        project_name (str): 项目名
        rename (str): 测试文件夹改名
        path (Path): 在测试文件夹中的位置
    """
    test_init = TEST_PATH.joinpath("__init__.py")
    if not test_init.exists():
        shutil.copy(
            str(PMFP_TEST_TEMP.joinpath("python/init.temp")),
            str(TEST_PATH.joinpath("__init__.py"))
        )
    test_const = TEST_PATH.joinpath("const.py")
    if not test_const.exists():
        shutil.copy(
            str(PMFP_TEST_TEMP.joinpath("python/const.py.temp")),
            str(TEST_PATH.joinpath("const.py"))
        )
    test_path = TEST_PATH.joinpath(f"test_{rename}")
    shutil.copytree(
        str(PMFP_TEST_TEMP.joinpath(path)),
        str(test_path)
    )
    iter_template_2_file(project_name, test_path)


def js_test(project_name: str, rename: str, path: Path):
    """为js组件创建测试.

    Args:
        project_name (str): 项目名
        rename (str): 测试文件夹改名
        path (Path): 在测试文件夹中的位置
    """
    test_init = TEST_PATH.joinpath("test.js.temp")
    if not test_init.exists():
        shutil.copy(
            str(PMFP_TEST_TEMP.joinpath("javascript/test.js.temp")),
            str(TEST_PATH.joinpath("test.js"))
        )

    test_const = TEST_PATH.joinpath("const.js.temp")
    if not test_const.exists():
        shutil.copy(
            str(PMFP_TEST_TEMP.joinpath("javascript/const.js.temp")),
            str(TEST_PATH.joinpath("const.js"))
        )

    test_path = TEST_PATH.joinpath(f"test_{rename}")
    shutil.copytree(
        str(PMFP_TEST_TEMP.joinpath(path)),
        str(test_path)
    )

    iter_template_2_file(project_name, test_path)


def new_test(language: str, project_name: str, rename: str):
    """各种语言的基本测试模板.

    Args:
        language ([type]): 标明语言.
    """

    if language == "Python":
        path = "python/universal/submodule"
        if not PMFP_TEST_TEMP.joinpath(path).exists():
            print(f"未找到{path}对应的测试")
            return
        print("创建相应的测试组件")
        if TEST_PATH.exists():
            if TEST_PATH.is_file():
                print("test不是文件夹")
                return
        else:
            TEST_PATH.mkdir()
            print("创建测试文件夹")
        python_test(project_name, rename, path)

    elif language == "Javascript":
        path = "javascript/universal/class_model.js.temp"
        if not PMFP_TEST_TEMP.joinpath(path).exists():
            print(f"未找到{path}对应的测试")
            return
        print("创建相应的测试组件")
        if TEST_PATH.exists():
            if TEST_PATH.is_file():
                print("test不是文件夹")
                return
        else:
            TEST_PATH.mkdir()
            print("创建测试文件夹")
        js_test(project_name, rename, path)
