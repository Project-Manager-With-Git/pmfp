"""执行golang的build操作."""
import os
import subprocess
from typing import Dict, Any, Optional
import chardet
from pmfp.const import PLATFORM, PROJECT_HOME


def build_go_app(name: str, entry: str, cross: Optional[str] = None) -> None:
    default_environ = dict(os.environ)
    if not PROJECT_HOME.joinpath("bin").is_dir():
        PROJECT_HOME.joinpath("bin").mkdir()
    if cross is None:
        if PLATFORM == 'Windows':
            target_name = f"{name}.exe"
        if not entry:
            command = f"go build -o bin/{target_name}"
        else:
            command = f"go build -o bin/{target_name} {entry}"
        env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
        env.update(**default_environ)
        res = subprocess.run(command, capture_output=True, shell=True,env=env)
        if res.returncode == 0:
            print(f"完成编译golang项目{name}!")
        else:
            print(f"交叉编译golang项目{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        GOOS, GOARCHS = cross.split("-")
        env = {"GOOS": GOOS, "GOARCHS": GOARCHS,"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
        env.update(**default_environ)
        dir_name = f"{GOOS}-{GOARCHS}"
        target_dir = PROJECT_HOME.joinpath("bin").joinpath(dir_name)
        if not target_dir.is_dir():
            target_dir.mkdir()
        target_name = name
        if GOOS == "windows":
            target_name = f"{name}.exe"
        if not entry:
            command = f"go build -o {str(target_dir)}/{target_name}"
        else:
            command = f"go build -o {str(target_dir)}/{target_name} {entry}"
        res = subprocess.run(command, capture_output=True, shell=True, env=env)
        if res.returncode == 0:
            print(f"已完成为{GOARCHS}平台的{GOOS}系统交叉编译golang项目{name}!")
        else:
            print(f"交叉编译golang项目{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))


def build_go_module(
        name: str,
        entry: str,
        cross: Optional[str] = None) -> None:
    if not PROJECT_HOME.joinpath("plugins").is_dir():
        PROJECT_HOME.joinpath("plugins").mkdir()
    if cross is None:
        target_name = f"{name}.plugin"
        if not entry:
            command = f"go build -buildmode=plugin -o plugins/{target_name} {name}"
        else:
            command = f"go build -buildmode=plugin -o plugins/{target_name} {entry}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"完成编译golang 插件模块{name}!")
        else:
            print(f"交叉编译golang 插件模块{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        GOOS, GOARCHS = cross.split("-")
        default_environ = dict(os.environ)
        env = {"GOOS": GOOS, "GOARCHS": GOARCHS}
        env.update(**default_environ)
        dir_name = f"{GOOS}-{GOARCHS}"
        target_dir = PROJECT_HOME.joinpath("plugins").joinpath(dir_name)
        if not target_dir.is_dir():
            target_dir.mkdir()
        target_name = name
        if not entry:
            command = f"go build -buildmode=plugin -o {str(target_dir)}/{target_name} {name}"
        else:
            command = f"go build -buildmode=plugin -o {str(target_dir)}/{target_name} {entry}"
        res = subprocess.run(
            command, capture_output=True, shell=True, env=env)
        if res.returncode == 0:
            print(f"已完成为{GOARCHS}平台的{GOOS}系统交叉编译golang的插件项目{name}!")
        else:
            print(f"交叉编译golang插件项目{name}失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))


def build_go(config: Dict[str, Any], cross: Optional[str] = None) -> None:
    """执行go项目下的`build`命令."""
    print("编译 golang 项目")
    name = config["project-name"]
    entry = config["entry"]
    project_type = config["project-type"]
    if project_type == "module":
        build_go_module(name=name, entry=entry, cross=cross)
    else:
        build_go_app(name=name, entry=entry, cross=cross)
