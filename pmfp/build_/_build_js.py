"""执行js的build操作."""
import subprocess
import chardet


def build_js() -> None:
    """执行js项目下package.json中定义的`build`命令."""
    print("编译转换js项目")
    command = "npm run build"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode == 0:
        print(f"完成编译转换js项目!")
    else:
        print(f"编译转换js项目失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
