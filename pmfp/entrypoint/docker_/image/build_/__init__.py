"""ppm docker image build命令的处理."""
from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from .core import dockerimage_build


@dockerimage_build.as_main
def build_dockerimage(docker_register_namespace: str, project_name: str, version: str,
                      dockerfile_name: str = "Dockerfile", docker_register: Optional[str] = None,
                      as_latest_img: bool = False, push: bool = False, cross_compiling: bool = False,
                      platform: List[str] = ["linux/amd64", "linux/arm64", "linux/arm/v7"],
                      cwd: str = ".", use_sudo: bool = False, sudo_pwd: Optional[str] = None) -> None:
    cwdp = get_abs_path(cwd)
    if docker_register:
        docker_register = docker_register + "/"
    else:
        docker_register = ""
    image_name = f"{docker_register}{docker_register_namespace}/{project_name}"

    if cross_compiling is False:
        tags = f" -t {image_name}:amd64-{version}"
        if as_latest_img:
            tags += f" -t {image_name}:amd64-latest"
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo  -p {sudo_pwd} docker build -f {dockerfile_name}{tags} ."
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"sudo docker build -f {dockerfile_name}{tags} ."
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"docker build -f {dockerfile_name}{tags} ."
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    else:
        for p in platform:
            ps = p.split("/")
            if len(ps) == 2:
                plat = ps[1]
            elif len(ps) == 3:
                plat = ps[1] + ps[2]
            else:
                raise AttributeError(f"unknown platform {platform}")
            tags = f" -t {image_name}:{plat}-{version}"
            if as_latest_img:
                tags += f" -t {image_name}:{plat}-latest"

            if use_sudo is True:
                if sudo_pwd is not None:
                    cmd = f"sudo -p {sudo_pwd} docker buildx build --load  --platform={p} -f {dockerfile_name}{tags} ."
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                else:
                    cmd = f"sudo -p docker buildx build --load  --platform={p} -f {dockerfile_name}{tags} ."
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"docker buildx build --load  --platform={p} -f {dockerfile_name}{tags} ."
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
