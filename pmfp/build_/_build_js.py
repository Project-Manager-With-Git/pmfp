"""执行js的build操作."""
import subprocess


def build_js() -> None:
    """执行js项目下package.json中定义的`build`命令."""
    print("编译转换js项目")
    command = "npm run build"
    subprocess.check_call(command, shell=True)
    print("完成编译转换js项目!")
