"""执行js的build操作."""
import subprocess


def build_js()->None:
    """执行js项目下package.json中定义的`build`命令."""
    print("build js project")
    command = "npm run build"
    subprocess.check_call(command, shell=True)
    print("build node project done!")
