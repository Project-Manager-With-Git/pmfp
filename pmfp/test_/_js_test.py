"""测试js项目."""
import chardet
import subprocess


def run_js_test():
    """测试js项目."""
    command = "npm run test"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("单元测试出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print("单元测试结果!")
        encoding = chardet.detect(res.stdout).get("encoding")
        print(res.stdout.decode(encoding))
    return True
