"""新建一个组件."""
from typing import Dict, Any
from pmfp.const import (
    GOLBAL_PYTHON_VERSION
)
from pmfp.utils import (
    get_golang_version,
    get_node_version
)
from ._new_component import new_component
from ._new_doc import new_document
from ._new_env import new_env
from ._new_setup import new_setup
from ._new_readme import new_readme
from ._new_pb import new_pb
from ._new_es_script import new_es_script
from ._new_test import new_test


def new(config: Dict[str, Any], kwargs: Dict[str, Any]):
    """新建一个组件.

    Args:
        config (Dict[str, Any]): 项目配置
        kwargs (Dict[str, Any]): 组件配置

    Raises:
        e: 组件创建错误

    """
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
    elif c_name in ("pb", "grpc", "grpc-streaming", "grpc-web-proxy"):
        if kwargs["rename"] == "-":
            rename = config["project-name"]
        elif kwargs["rename"] == "":
            rename = c_name
        else:
            rename = kwargs["rename"]
        new_pb(c_name=c_name, rename=rename, to=to, project_name=config["project-name"])
    elif c_name == "test":
        project_name = config["project-name"]
        if kwargs["rename"] == "-":
            rename = config["project-name"]
        elif kwargs["rename"] == "":
            rename = c_name
        else:
            rename = kwargs["rename"]
        new_test(c_language, project_name, rename)
    elif c_name == "es_script" and c_language == "Javascript":
        new_es_script(config)
    else:
        if not kwargs.get("kwargs"):
            kwargs["kwargs"] = {}
        if c_language == "Golang":
            kwargs["kwargs"]["language_version"] = get_golang_version() or "latest"
        elif c_language == "Python":
            kwargs["kwargs"]["language_version"] = GOLBAL_PYTHON_VERSION or "latest"
        elif c_language == "Javascript":
            kwargs["kwargs"]["language_version"] = get_node_version() or "latest"
        spl_name = c_name.split("-")
        c_category = spl_name[0]
        c_name = "".join(spl_name[1:])
        if kwargs["rename"] == "-":
            rename = config["project-name"]
        elif kwargs["rename"] == "":
            rename = c_name
        else:
            rename = kwargs["rename"]
        c_language = c_language.lower()
        c_path = f"{c_language}/{c_category}/{c_name}"
        test = kwargs["test"]
        try:
            nc_kwargs = kwargs.get("kwargs", {})
            print(f"创建组件{c_path},kwargs: {nc_kwargs}")
            new_component(
                config,
                path=c_path,
                to=to,
                rename=rename,
                test=test,
                **nc_kwargs)
        except Exception as e:
            print(f"组件{c_path}创建错误")
            raise e
        else:
            print(f"{c_path}创建为{rename}成功")
