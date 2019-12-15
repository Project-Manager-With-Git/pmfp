"""将python项目发布到合适的地方."""
import subprocess
import chardet
from pathlib import Path
from typing import Dict, Any
from pmfp.freeze import freeze
from pmfp.build_ import build
from pmfp.const import PROJECT_HOME


def release_py(config: Dict[str, Any]) -> None:
    """将python项目发布到合适的地方.

    目前模块项目会被发送到pypi,application则会打包为docker image发送到指定的远程register.

    Args:
        config (Dict[str, Any]): 项目的配置字典

    Raises:
        AttributeError: 没有dockerfile
        AttributeError: 没有指定镜像仓库,请在pmfprc.json中指定remote_registry
        AttributeError: pypi upload should have a .pypirc file in home path

    """
    home = Path.home()
    if config["project-type"] == "module":
        if home.joinpath(".pypirc").exists():
            if not PROJECT_HOME.joinpath("requirements.txt").exists():
                print("没有requirements.txt,创建")
                freeze(config, {})
            command = "python setup.py sdist upload"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("发布sdist包到pypi失败")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("发布sdist包到pypi成功!")
            command = "python setup.py bdist_wheel upload"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("发布bdist_wheel包到pypi失败")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("发布bdist_wheel包到pypi成功!")

        else:
            raise AttributeError("pypi upload 需要设置文件`.pypirc`")
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
            freeze(config, {})
        if PROJECT_HOME.joinpath(config["project-name"]).exists():
            print("打包项目为pyz")
            build(config)
            print("打包项目为pyz成功")
        image_name = project_name.lower()
        command = f"docker build --pull -t {remote_registry}/{image_name}:{status}-{version} ."
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print("项目打包为docker镜像失败")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print("项目打包为docker镜像成功!")
            command = f"docker push {remote_registry}/{image_name}:{status}-{version}"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("项目docker镜像提交到镜像仓库失败")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("成功将项目docker镜像提交到镜像仓库!")
