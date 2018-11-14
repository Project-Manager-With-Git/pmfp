from pathlib import Path
from .new_component import new_component
from .new_doc import new_document
from .new_env import new_env
from .new_setup import new_setup
from .new_readme import new_readme
from .new_pb import new_pb


def new(config, kwargs):
    if kwargs["language"] == "-":
        c_language = config["project-language"]
    else:
        c_language = kwargs["language"]

    if kwargs["to"] == "-":
        to = config["project-name"]
    else:
        to = kwargs["to"]
    c_name = kwargs["component_name"]
    

    if c_name in ("document", "doc"):
        new_document(config, c_language.lower())
    elif c_name == "env":
        new_env(config, c_language.lower())
    elif c_name == "readme":
        new_readme(config)
    elif c_name in ("setup", "cython_setup", "cython_numpy_setup", "cmd_setup"):
        new_setup(config, c_language, c_name)
    elif c_name in ("pb","grpc"):
        if kwargs["rename"] == "-":
            rename = config["project-name"]
        elif kwargs["rename"] == "":
            rename = c_name
        else:
            rename = kwargs["rename"]
        new_pb(c_name,rename,to)

    else:
        spl_name = c_name.split("-")
        c_category = spl_name[0]
        c_name = "".join(spl_name[1:])
        if kwargs["rename"] == "-":
            rename = config["project-name"]
        elif kwargs["rename"] == "":
            rename = c_name
        else:
            rename = kwargs["rename"]
        c_path = f"{c_language}/{c_category}/{c_name}"
        test = kwargs["test"]
        try:
            print(f"创建组件{c_path}")
            new_component(config, path=c_path, to=to, rename=rename, test=test)
        except Exception as e:
            print(f"组件{c_path}创建错误")
            raise e
        else:
            print(f"{c_path}创建为{rename}成功")
