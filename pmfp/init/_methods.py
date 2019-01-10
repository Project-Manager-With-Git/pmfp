import json
from pmfp.new import new
from pmfp.clean import clean
from pmfp.install import install
from pmfp.utils import find_template_path


def _init_env(config, test=False, doc=False):
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


def _init_readme(config, test=False, doc=False):
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


def _init_requirement(config, test, doc):
    t_path = find_template_path(config)
    with open(str(t_path),encoding="utf-8") as f:
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


def _init_component(config, test, doc):
    t_path = find_template_path(config)
    with open(str(t_path),encoding="utf-8") as f:
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


def _init_doc(config, test, doc):
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


def _init_esscript(config, test, doc):
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


def init(config, test=False, doc=False):
    try:
        _init_env(config, test, doc)
        _init_readme(config, test, doc)
        _init_requirement(config, test, doc)
        _init_component(config, test, doc)
        if doc is True:
            _init_doc(config, test, doc)
        if config["project-language"] == "Javascript":
            _init_esscript(config, test, doc)
    except Exception as e:
        print(f"初始化因{type(e)}错误{str(e)}中断")
        clean(total=True)
        raise e
