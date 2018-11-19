import subprocess
from pathlib import Path
from pmfp.freeze import freeze
from pmfp.build_ import build
from pmfp.const import PROJECT_HOME

def release_py(config):
    home = Path.home()
    if home.joinpath(".pypirc").exists():
        if config["project-type"] == "module":
            if not PROJECT_HOME.joinpath("requirements.txt").exists():
                print("没有requirements.txt,创建")
                freeze(config)
            command = "python setup.py sdist upload"
            subprocess.check_call(command, shell=True)
            command = "python setup.py bdist_wheel upload"
            subprocess.check_call(command, shell=True)
            print("release package to pypi done!")
        else:
            project_name = config["project-name"]
            remote_registry = config["remote_registry"]
            version = config["version"]
            status = config["status"]
            if not PROJECT_HOME.joinpath("dockerfile").exists():
                print("没有dockerfile")
                raise AttributeError("没有dockerfile")
            if not remote_registry:
                print("没有指定镜像仓库,请在pmfprc.json中指定remote_registry")
                raise AttributeError("没有指定镜像仓库,请在pmfprc.json中指定remote_registry")
            if not PROJECT_HOME.joinpath("requirements.txt").exists():
                print("没有requirements.txt,创建")
                freeze(config)
            if PROJECT_HOME.joinpath(config["project-name"]).exists():
                print("打包项目为pyz")
                build(config)
                print("打包项目为pyz成功")
            image_name = project_name.lower()
            command = f"docker build --pull -t {remote_registry}/{image_name}:{status}-{version} ."
            subprocess.check_call(command, shell=True)
            command = f"docker push {remote_registry}/{image_name}:{status}-{version}"
            subprocess.check_call(command, shell=True)
            print("release package to docker registry done!")
    else:
        raise AttributeError("pypi upload should have a .pypirc file in home path")