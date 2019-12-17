"""执行golang的build操作."""
import subprocess
from typing import Dict, Any, Optional
import chardet
from pmfp.const import PLATFORM, PROJECT_HOME


def build_go_app(name: str, entry: str, cross: Optional[str] = None) -> None:
    if not PROJECT_HOME.joinpath("bin").is_dir():
        PROJECT_HOME.joinpath("bin").mkdir()
    if cross is None:
        if PLATFORM == 'Windows':
            target_name = f"{name}.exe"
        if not entry:
            command = f"go build -o bin/{target_name}"
        else:
            command = f"go build -o bin/{target_name} {entry}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"完成编译golang项目{name}!")
        else:
            print(f"交叉编译golang项目{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        GOOSS, GOARCHS = cross.split("-")
        dir_name = f"{GOOSS}-{GOARCHS}"
        target_dir = PROJECT_HOME.joinpath("bin").joinpath(dir_name)
        if not target_dir.is_dir():
            target_dir.mkdir()
        target_name = name
        if GOOSS == "windows":
            target_name = f"{name}.exe"
        if not entry:
            command = f"GOOS={GOOSS} GOARCH={GOARCHS} go build -o {str(target_dir)}/{target_name}"
        else:
            command = f"GOOS={GOOSS} GOARCH={GOARCHS} go build -o {str(target_dir)}/{target_name} {entry}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"已完成为{GOARCHS}平台的{GOOSS}系统交叉编译golang项目{name}!")
        else:
            print(f"交叉编译golang项目{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))


def build_go_module(
        name: str,
        entry: str,
        cross: Optional[str] = None,
        asdll: bool = False) -> None:
    # if not PROJECT_HOME.joinpath("lib").is_dir():
    #     PROJECT_HOME.joinpath("lib").mkdir()
    if asdll:
        pass
    else:
        if cross is None:
            command = f"go install"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode == 0:
                print(f"完成编译golang 静态模块{name}!")
            else:
                print(f"交叉编译golang 静态模块{name}失败!")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
        else:
            GOOSS, GOARCHS = cross.split("-")
            dir_name = f"{GOOSS}-{GOARCHS}"

            if GOOSS == "windows":
                target_name = f"{name}.exe"
            if not entry:
                command = f"go build -o {str(target_dir)}/{target_name}"
            else:
                command = f"go build -o {str(target_dir)}/{target_name} {entry}"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode == 0:
                print(f"已完成为{GOARCHS}平台的{GOOSS}系统交叉编译golang项目{name}!")
            else:
                print(f"交叉编译golang项目{name}失败!")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))


def build_go(config: Dict[str, Any], cross: Optional[str] = None, asdll: bool = False) -> None:
    """执行go项目下的`build`命令."""
    print("编译 golang 项目")
    name = config["project-name"]
    entry = config["entry"]
    project_type = config["project-type"]
    if project_type == "module":
        pass
    else:
        build_go_app(name=name, entry=entry, cross=cross)
