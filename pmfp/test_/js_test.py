import subprocess


def run_js_test():
    """测试项目"""
    command = "npm run test"
    subprocess.check_call(command, shell=True)
    return True
