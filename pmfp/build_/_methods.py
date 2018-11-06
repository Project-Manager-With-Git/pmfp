from .build_js import build_js
from .build_python import (
    build_python_app,
    build_python_module
)


def build(config):
    project_name = config["project-name"]
    language = config["project-language"]
    env = config["env"]
    gcc = config["gcc"]
    type_ = config["project-type"]
    if language == "Python":
        if type_ == "application":
            build_python_app(project_name)
        else:
            build_python_module(project_name)
    elif language == "Javascript":
        build_js()
