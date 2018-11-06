import subprocess


def build_js():
    print("build js project")
    command = "npm run build"
    subprocess.check_call(command, shell=True)
    print("build node project done!")
