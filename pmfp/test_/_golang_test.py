"""测试js项目."""

import subprocess


def run_golang_test(config, benchmark):
    """测试golang项目."""
    pname = config["project-name"]
    if not benchmark:

        command = "go test -v -cover {pname}"
        subprocess.check_call(command, shell=True)
        return True
    else:
        command = f"go test -v -benchmem -run=^$ {pname} -bench ."
        subprocess.check_call(command, shell=True)
