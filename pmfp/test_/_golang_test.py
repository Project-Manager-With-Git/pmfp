"""测试js项目."""
import chardet
import subprocess


def run_golang_test(config, benchmark):
    """测试golang项目."""
    pname = config["project-name"]
    if not benchmark:

        command = "go test -v -cover {pname}"
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
    else:
        command = f"go test -v -benchmem -run=^$ {pname} -bench ."
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print("基准测试出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print("基准测试结果!")
            encoding = chardet.detect(res.stdout).get("encoding")
            print(res.stdout.decode(encoding))
