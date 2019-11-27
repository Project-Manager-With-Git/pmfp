"""执行golang的build操作."""
import subprocess
from pmfp.const import PLATFORM, PROJECT_HOME


def build_go(config, cross=None) -> None:
    """执行go项目下的`build`命令."""
    print("编译 golang 项目")
    name = config["project-name"]
    if not PROJECT_HOME.joinpath("bin").is_dir():
        PROJECT_HOME.joinpath("bin").mkdir()

    if cross is None:
        if PLATFORM == 'Windows':
            target_name = f"{name}.exe"
        command = f"go build -o bin/{target_name}"
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
        command = f"go build -o {str(target_dir)}/{target_name}"
        subprocess.check_call(command, shell=True)
        print(f"已完成为{GOARCHS}平台的{GOOSS}系统交叉编译golang项目{name}!")
