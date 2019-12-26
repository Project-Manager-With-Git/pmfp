"""将js项目发布到合适的地方."""
import subprocess
import chardet
from pathlib import Path
from typing import Dict, Any
from pmfp.const import PROJECT_HOME


def release_golang(config: Dict[str, Any]) -> None:
    """将go项目发布到合适的地方.

    目前模块项目会被发送到npm,application则会打包为docker image发送到指定的远程register.

    Args:
        config (Dict[str, Any]): 项目的配置字典

    Raises:
        AttributeError: 没有package.json
        AttributeError: 没有dockerfile
        AttributeError: 没有指定镜像仓库,请在pmfprc.json中指定remote_registry
        AttributeError: pypi upload should have a .pypirc file in home path

    """
    home = Path.home()
    if config["project-type"] == "module":
        print("golang没有包仓库,请使用`upload -t`接口上传源文件到git仓库")
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
        command = f"docker build --pull -t {remote_registry}/{project_name}:{status}-{version} ."
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print("项目打包为docker镜像失败")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print('项目打包为docker镜像成功!')
            command = f"docker push {remote_registry}/{project_name}:{status}-{version}"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print("go语言项目的docker镜像上传失败")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                print("成功将项目docker镜像提交到镜像仓库!")
