import shutil
from string import Template
from pathlib import Path
from pmfp.const import (
    PMFP_COMPONENTS_HOME,
    PROJECT_HOME,
    TEST_PATH,
    PMFP_TEST_TEMP
)


def template_2_file(project_name, path):
    """注意rename是名字不含后缀

    Args:
        path ([type]): [description]
        rename ([type], optional): Defaults to None. [description]
    """

    if (".py" in path.name) or (
            ".js" in path.name) or (
            ".ts" in path.name) or (
            ".c" in path.name) or (
            ".cpp" in path.name) or (
            ".go" in path.name) or (
            "docker" in path.name) or (
            ".json" in path.name):
        try:
            template_content = Template(path.open().read())
            content = template_content.substitute(
                project_name=project_name
            )
        except:
            print(f"path:{path} template2file error")
            raise
        else:
            path.open("w").write(content)
    else:
        try:
            content = path.open("r").read()
        except UnicodeDecodeError as e:
            content = path.open("rb").read()
            path.open("wb").write(content)
        else:
            path.open("w").write(content)
    newpath = str(path).replace(".temp", "")
    path.rename(Path(newpath))


def iter_template_2_file(project_name, path):
    for p in path.iterdir():
        if p.is_file():
            if p.suffix == ".temp":
                template_2_file(project_name, p)
        else:
            iter_template_2_file(project_name, p)


def new_component(config, path, to, rename, test):
    project_name = config["project-name"]
    c_path = PMFP_COMPONENTS_HOME.joinpath(path)
    t_path = PROJECT_HOME.joinpath(to)
    if not c_path.exists():
        print(f"找不到对应的组件{str(c_path)}")
        return
    if not t_path.exists():
        print(f"找不到目标目录{str(t_path)},新建")
        t_path.mkdir(parents=True, exist_ok=False)

    if c_path.is_file():
        name = c_path.name
        suname = c_path.stem
        purename = Path(suname).stem
        suffixe = Path(suname).suffix
        to_path = t_path.joinpath(rename + suffixe)
        if to_path.exists():
            print(f"存在同名组件{rename}")
            return
        else:
            # to = t_path.joinpath(name)
            shutil.copy(
                str(c_path),
                str(to_path)
            )
            template_2_file(project_name, to_path)
    else:
        to_path = t_path.joinpath(rename)
        if t_path.joinpath(rename).exists():
            print(f"存在同名组件{rename}")
            return
        else:
            shutil.copytree(
                str(c_path),
                str(to_path)
            )
            iter_template_2_file(project_name, to_path)
    if test is True:
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

        if config["project-language"] == "Python":
            test_init = TEST_PATH.joinpath("__init__.py")
            if not test_init.exists():
                shutil.copy(
                    str(PMFP_TEST_TEMP.joinpath("python/init.temp")),
                    str(TEST_PATH.joinpath("__init__.py"))
                )
                # template_2_file(project_name, TEST_PATH.joinpath("__init__.py"))
                # with open(str(test_init), "w") as f:
                #     content = PMFP_TEST_TEMP.joinpath("python/init.temp").open().read()
                #     f.write(content)
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

        else:
            print("语言不支持测试")
