import subprocess
from pmfp.utils import get_python_path
def run(config,cmd):
    if config["project-language"] == "Python":
        entry = config["entry"]
        if not entry:
            print("请先在配置文件中指定入口")
            return 
        python = get_python_path(config)
        if cmd:
            command = f"{python} {entry} {cmd}"
        else:
            command = f"{python} {entry}"
        subprocess.check_call(command, shell=True)
    elif config["project-language"] == "Javascript":
        pass
