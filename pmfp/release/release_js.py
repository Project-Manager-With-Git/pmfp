import subprocess
from pmfp.const import PROJECT_HOME


def release_js(config):
    home = Path.home()
    if home.joinpath(".pypirc").exists():
        if config["project-type"] == "module":
            if not PROJECT_HOME.joinpath("package.json").exists():
                print("没有package.json")
                raise AttributeError("package.json")
            command = "npm publish"
            subprocess.call(command, shell=True)
            print("release package to npm done!")
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
            subprocess.check_call(command, shell=True)
            command = f"docker push {remote_registry}/{project_name}:{status}-{version}"
            subprocess.check_call(command, shell=True)
            print("release package to docker registry done!")
    else:
        raise AttributeError("pypi upload should have a .pypirc file in home path")
