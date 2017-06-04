from .Data import Dockerfile
from .utils import read_ppmrc, project_form
from pathlib import Path
import subprocess
from typing import Dict, Optional
from argparse import Namespace


def project_info()->Dict[str, Dict[str, str]]:
    conf = read_ppmrc()
    project = conf.items("project")
    form = project_form()
    result = dict(project)
    result.update(form=project_form())
    return result


def dockerfile_exist()->bool:
    dockerfilepath = Path(".").absolute().joinpath("Dockerfile")
    if dockerfilepath.exists():
        return True
    else:
        return False


def init_dockerfile()->int:

    if dockerfile_exist():
        print('dockerfile already exists!')
        return 0
    info = project_info()
    if info[form] == "model":
        print("model do not need to build a docker img!")
        return 0
    if info[form] == "script":
        suffix = "py"

    if info[form] in ["web", "command", "gui"]:
        suffix = "pyz"

    if not Path(project_name + suffix).absolute.exists():
        print("do not have the main file:" + info["project_name"] + suffix)
        return 0

    dockerfile = Dockerfile.substitute(v1=str(sys.version_info[0]),
                                       v2=str(sys.version_info[1]),
                                       project_name=info["project_name"],
                                       suffix=suffix)
    with open('Dockerfile', "w") as f:
        f.write(dockerfile)
    return 1


def build_docker()->int:
    if not dockerfile_exist():
        print("need a dockerfile!")
        return 0

    info = project_info()
    subprocess.check_call(
        ['docker', 'build', "-t", info["project_name"] + ":" + info["version"], "."])
    return 1


def push_docker(url: Optional[str]=None)->int:
    if not dockerfile_exist():
        print("need a dockerfile!")
        return 0
    if url == None:
        info = project_info()
        print("push the img to docker hub")
        subprocess.check_call(
            ['docker', 'push', info["project_name"] + ":" + info["version"]])
        print("push the img to docker done!")
    else:
        info = project_info()
        print("push the img to " + url)
        subprocess.check_call(['docker', 'tag', info["project_name"] + ":" +
                               info["version"], url + info["project_name"] + ":" + info["version"]])
        subprocess.check_call(
            ['docker', 'push', url + info["project_name"] + ":" + info["version"]])
        print("push the img to " + url + " done!")


def docker(args: Namespace)->int:
    if args.init:
        init_dockerfile()

    elif args.build:
        build_docker()
    elif args.push or args.push == []:
        if args.push == []:
            push_docker()
        else:
            url = args.push
            push_docker(url)
    return 1
