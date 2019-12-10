"""执行golang的build操作."""
import subprocess
from typing import Dict, Any, Optional
from pmfp.const import PLATFORM, PROJECT_HOME


def build_go(config: Dict[str, Any], cross: Optional[str] = None) -> None:
    """执行go项目下的`build`命令."""
    print("编译 golang 项目")
    name = config["project-name"]
    entry = config["entry"]
    project_type = config["project-type"]
    if project_type == "module":
        pass
    else:
        if not PROJECT_HOME.joinpath("bin").is_dir():
            PROJECT_HOME.joinpath("bin").mkdir()

        if cross is None:
            if PLATFORM == 'Windows':
                target_name = f"{name}.exe"
            if not entry:
                command = f"go build -o bin/{target_name}"
            else:
                command = f"go build -o bin/{target_name} {entry}"
            subprocess.check_call(command, shell=True)
            print("完成编译golang项目{name}!")
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
                command = f"go build -o {str(target_dir)}/{target_name}"
            else:
                command = f"go build -o {str(target_dir)}/{target_name} {entry}"
            subprocess.check_call(command, shell=True)
            print(f"已完成为{GOARCHS}平台的{GOOSS}系统交叉编译golang项目{name}!")
