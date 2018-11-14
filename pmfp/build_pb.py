import subprocess


def build_pb(config, kwargs):
    name = kwargs.get("name")
    dir_ = kwargs.get("dir")
    default_lang = config["project-language"].lower() if config["project-language"] != "Javascript" else "js"
    language = default_lang if not kwargs.get("language") else kwargs.get("language")
    grpc = kwargs.get("grpc")
    to = kwargs.get("to") if kwargs.get("to") else config["project-name"]
    if grpc:
        command = f"python -m grpc_tools.protoc -I{dir_} --{language}_out={to} --grpc_{language}_out={to} {name}"
    else:
        command = f"protoc -I={dir_} --{language}_out={to} {dir_}/{name}"
    subprocess.check_call(command, shell=True)
