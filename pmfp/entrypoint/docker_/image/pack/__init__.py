"""ppm docker image pack命令的处理."""
from typing import List, Optional
from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from .core import dockerimage_pack


def pack(image_name: str, version: str, cwdp: Path, push: bool = False,
         platform: List[str] = ["linux/amd64", "linux/arm64", "linux/arm/v7"],
         use_sudo: bool = False, sudo_pwd: Optional[str] = None) -> None:
    cmd_content = ""
    for p in platform:
        ps = p.split("/")
        if len(ps) == 2:
            plat = ps[1]
        elif len(ps) == 3:
            plat = ps[1] + ps[2]
        else:
            raise AttributeError(f"unknown platform {platform}")
        cmd_content += f" {image_name}:{plat}-{version}"
    if use_sudo is True:
        if sudo_pwd is not None:
            cmd = f"sudo -p {sudo_pwd} docker manifest create {image_name}:{version}{cmd_content}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"sudo docker manifest create {image_name}:{version}{cmd_content}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    else:
        cmd = f"docker manifest create {image_name}:{version}{cmd_content}"
        run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    if push:
        cmd = "docker push -a image_name"
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo -p {sudo_pwd} docker push -a image_name"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = "sudo docker push -a image_name"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = "docker push -a image_name"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)


@dockerimage_pack.as_main
def pack_dockerimage(docker_register_namespace: str, project_name: str, version: str,
                     docker_register: Optional[str] = None,
                     as_latest_img: bool = False, push: bool = False,
                     platform: List[str] = ["linux/amd64", "linux/arm64", "linux/arm/v7"],
                     cwd: str = ".", use_sudo: bool = False, sudo_pwd: Optional[str] = None) -> None:
    cwdp = get_abs_path(cwd)
    image_name = f"{docker_register}/{docker_register_namespace}/{project_name}"
    pack(image_name=image_name, version=version, cwdp=cwdp, push=push,
         platform=platform,
         use_sudo=use_sudo, sudo_pwd=sudo_pwd)
    if as_latest_img:
        pack(image_name=image_name, version="latest", cwdp=cwdp, push=push,
             platform=platform,
             use_sudo=use_sudo, sudo_pwd=sudo_pwd)
