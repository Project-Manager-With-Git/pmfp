import json
from pmfp.new import new
from pmfp.clean import clean
from pmfp.install import install
from pmfp.utils import find_template_path


def init(config, test=False, doc=False):
    try:
        t_path = find_template_path(config)
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
        print("创建文档")
        readme_kwargs = {
            "component_name": "readme",
            'to': "-",
            'rename': "-",
            "language": "-",
            "test": False
        }
        new(config, readme_kwargs)
        print("文档创建完成")
        with open(str(t_path)) as f:
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
        if doc is True:
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
    except Exception as e:
        print(f"初始化因{type(e)}错误{str(e)}中断")
        clean(total=False)
