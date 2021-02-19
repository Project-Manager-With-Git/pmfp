from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path_str
from invoke import Context
from .core import dockerfile_build


@dockerfile_build.as_main
def build_dockerfile(docker_register_namespace: str, project_name: str, version: str,
                     dockerfile_name: str = "Dockerfile", docker_register: Optional[str] = None,
                     as_latest_img: bool = False, push: bool = False, cross_compiling: bool = False,
                     platform: List[str] = ["linux/amd64", "linux/arm64", "linux/arm/v7"],
                     cwd: str = ".", use_sudo: bool = False, sudo_pwd: Optional[str] = None) -> None:
    cwdp = get_abs_path_str(cwd)
    image_name = f"{docker_register}/{docker_register_namespace}/{project_name}"
    ctx = Context()
    with ctx.cd(cwdp):
        if cross_compiling is False:
            tags = f" -t {image_name}:amd64-{version}"
            if as_latest_img:
                tags += f" -t {image_name}:amd64-latest"
            cmd = f"docker build -f {dockerfile_name}{tags} ."
            if use_sudo is True:
                if sudo_pwd is not None:
                    ctx.sudo(cmd, echo=True, password=sudo_pwd)
                ctx.sudo(cmd, echo=True)
            else:
                ctx.run(cmd, echo=True)

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
                cmd = f"docker buildx build --load  --platform={p} -f {dockerfile_name}{tags} ."
                if use_sudo is True:
                    if sudo_pwd is not None:
                        ctx.sudo(cmd, echo=True, password=sudo_pwd)
                    ctx.sudo(cmd, echo=True)
                else:
                    ctx.run(cmd, echo=True)
        if push:
            cmd = "docker push -a image_name"
            if use_sudo is True:
                if sudo_pwd is not None:
                    ctx.sudo(cmd, echo=True, password=sudo_pwd)
                ctx.sudo(cmd, echo=True)
            else:
                ctx.run(cmd, echo=True)
