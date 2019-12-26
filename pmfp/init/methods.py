"""init项目的公开方法."""

import json
from typing import Dict, Any
from pmfp.new import new
from pmfp.clean import clean
from pmfp.install import install
from pmfp.utils import find_template_path
from pmfp.const import PMFPRC_PATH


def _init_env(config: Dict[str, Any]) -> None:
    """初始化环境.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    print("创建虚拟环境")
    env_kwargs = {
        "component_name": "env",
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False
    }
    new(config, env_kwargs)
    print("虚拟环境创建完了")


def _init_readme(config: Dict[str, Any]) -> None:
    """初始化README文件.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    print("创建说明文档")
    readme_kwargs = {
        "component_name": "readme",
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False
    }
    new(config, readme_kwargs)
    print("说明文档创建完成")


def _init_requirement(config: Dict[str, Any]) -> None:
    """初始化依赖安装.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    t_path = find_template_path(config)
    with open(str(t_path), encoding="utf-8") as f:
        temp_info = json.load(f)
    print("安装开发依赖")
    for i in temp_info["requirement-dev"]:
        install_kwargs = {"dev": True, "package": i}
        install(config, install_kwargs)
    print("开发依赖安装完成")
    print("安装模板依赖")
    for i in temp_info["requirement"]:
        install_kwargs = {"dev": False, "package": i}
        install(config, install_kwargs)
    print("模板依赖安装完成")


def _init_requirement_noinstall(config: Dict[str, Any]) -> None:
    """初始化依赖但不安装.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    t_path = find_template_path(config)
    with open(str(t_path), encoding="utf-8") as f:
        temp_info = json.load(f)
    print("准备依赖")
    requirement_dev = temp_info["requirement-dev"]
    requirement = temp_info["requirement"]
    print("依赖准备完成")
    config["requirement-dev"] = requirement_dev
    config["requirement"] = requirement
    with open(str(PMFPRC_PATH), "w", encoding="utf-8") as f:
        json.dump(config, f)
    print("依赖写入完成")


def _init_component(config: Dict[str, Any], test: bool) -> None:
    """初始化组件.

    Args:
        config (Dict[str, Any]): 项目配置.
        test (bool): 组件使用带测试模板
    """
    t_path = find_template_path(config)
    with open(str(t_path), encoding="utf-8") as f:
        temp_info = json.load(f)
    print("安装组件")
    for component_name, (to, rename) in temp_info["components"].items():
        new_kwargs = {
            "component_name": component_name,
            'to': to,
            'rename': rename,
            "language": "-",
            "test": test
        }
        new(config, new_kwargs)
    print("安装组件完成")


def _init_doc(config: Dict[str, Any]) -> None:
    """初始化文档.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    print("创建文档")
    doc_kwargs = {
        "component_name": "doc",
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False
    }
    new(config, doc_kwargs)
    print("创建文档完成")


def _init_esscript(config: Dict[str, Any]) -> None:
    """初始化js环境的命令配置.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    print("创建js环境的执行命令")
    esscript_kwargs = {
        "component_name": "es_script",
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False
    }
    new(config, esscript_kwargs)
    print("创建js环境的执行命令完成")


def init(config: Dict[str, Any], test: bool = False, doc: bool = False, noinstall: bool = False) -> None:
    """初始化项目.

    Args:
        config (Dict[str, Any]): [description]
        test (bool, optional): Defaults to False. [description]
        doc (bool, optional): Defaults to False. [description]

    Raises:
        e: 初始化时报错

    """
    try:
        _init_component(config, test)
        _init_env(config)
        _init_readme(config)
        if not noinstall:
            _init_requirement(config)
        else:
            _init_requirement_noinstall(config)
        if doc is True:
            _init_doc(config)
        if config["project-language"] == "Javascript":
            _init_esscript(config)
    except Exception as e:
        print(f"初始化因{type(e)}错误{str(e)}中断")
        clean(total=True)
        raise e
