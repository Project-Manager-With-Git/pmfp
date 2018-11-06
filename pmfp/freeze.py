import subprocess
from pmfp.utils import get_python_path


def freeze(config):
    python_path = get_python_path(config)
    command = f"{python_path} -m pip freeze > requirements.txt"
    subprocess.check_call(command, shell=True)
    print("freeze完成")
