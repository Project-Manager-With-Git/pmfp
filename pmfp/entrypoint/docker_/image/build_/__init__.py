"""ppm docker image build命令的处理."""
from pathlib import Path
from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from .core import dockerimage_build


def build_no_cross_compiling(cwdp: Path, dockerfile_name: str, image_name: str, version: str,
                             as_latest_img: bool, push: bool, use_sudo: bool, sudo_pwd: Optional[str] = None) -> None:
    tags = f" -t {image_name}:{version}"
    if as_latest_img:
        tags += f" -t {image_name}:latest"
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
    if push:
        cmd = f"docker push -a {image_name}"
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo -p {sudo_pwd} docker push -a {image_name}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"sudo docker push -a {image_name}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"docker push -a {image_name}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)


def build_cross_compiling_only_manifest(cwdp: Path, dockerfile_name: str, image_name: str, version: str, platform: List[str],
                                        as_latest_img: bool, use_sudo: bool, sudo_pwd: Optional[str] = None) -> None:
    platformstr = ",".join(platform)
    tags = f" -t {image_name}:{version}"
    if as_latest_img:
        tags += f" -t {image_name}:latest"
    if use_sudo is True:
        if sudo_pwd is not None:
            cmd = f"sudo -p {sudo_pwd} docker buildx build --push --platform={platformstr} -f {dockerfile_name}{tags} ."
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"sudo -p docker buildx build --push  --platform={platformstr} -f {dockerfile_name}{tags} ."
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    else:
        cmd = f"docker buildx build --push --platform={platformstr} -f {dockerfile_name}{tags} ."
        run(cmd, cwd=cwdp, visible=True, fail_exit=True)


def build_cross_compiling(cwdp: Path, dockerfile_name: str, image_name: str, version: str, platform: List[str],
                          as_latest_img: bool, use_sudo: bool, push: bool, sudo_pwd: Optional[str] = None) -> None:
    versiontagslist = []
    latesttagslist = []
    tagslist = []
    for p in platform:
        ps = p.split("/")
        if len(ps) == 2:
            plat = ps[1]
        elif len(ps) == 3:
            plat = ps[1] + ps[2]
        else:
            raise AttributeError(f"unknown platform {platform}")
        version_tag = f"{image_name}:{plat}-{version}"
        tags = f" -t {version_tag}"
        versiontagslist.append(version_tag)
        if as_latest_img:
            latest_tag = f"{image_name}:{plat}-latest"
            tags += f" -t {latest_tag}"
            latesttagslist.append(latest_tag)
        tagslist.append(tags)

    for tags in tagslist:
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo -p {sudo_pwd} docker buildx build --load --platform={p} -f {dockerfile_name}{tags} ."
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"sudo -p docker buildx build --load --platform={p} -f {dockerfile_name}{tags} ."
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"docker buildx build --load --platform={p} -f {dockerfile_name}{tags} ."
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    if push:
        cmd = f"docker push -a {image_name}"
        # 推镜像
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo -p {sudo_pwd} docker push -a {image_name}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"sudo docker push -a {image_name}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"docker push -a {image_name}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        # 构造manifest
        imgstr = " ".join(versiontagslist)
        if use_sudo is True:
            if sudo_pwd is not None:
                cmd = f"sudo -p {sudo_pwd} docker manifest create --amend  {image_name}:{version} {imgstr}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                cmd = f"sudo -p {sudo_pwd} docker manifest push --purge {image_name}:{version}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"sudo docker manifest create --amend  {image_name}:{version} {imgstr}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                cmd = f"sudo docker manifest push --purge {image_name}:{version}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
        else:
            cmd = f"docker manifest create --amend {image_name}:{version} {imgstr}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            cmd = f"docker manifest push --purge {image_name}:{version}"
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)

        if as_latest_img:
            imgstr = " ".join(latesttagslist)
            if use_sudo is True:
                if sudo_pwd is not None:
                    cmd = f"sudo -p {sudo_pwd} docker manifest create --amend  {image_name}:latest {imgstr}"
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                    cmd = f"sudo -p {sudo_pwd} docker manifest push --purge {image_name}:latest"
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                else:
                    cmd = f"sudo docker manifest create --amend  {image_name}:latest {imgstr}"
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                    cmd = f"sudo docker manifest push --purge {image_name}:latest"
                    run(cmd, cwd=cwdp, visible=True, fail_exit=True)
            else:
                cmd = f"docker manifest create --amend  {image_name}:latest {imgstr}"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)
                cmd = f"docker manifest push --purge {image_name}:latest"
                run(cmd, cwd=cwdp, visible=True, fail_exit=True)


@dockerimage_build.as_main
def build_dockerimage(docker_register_namespace: str, project_name: str, version: str,
                      dockerfile_name: str = "Dockerfile", docker_register: Optional[str] = None,
                      as_latest_img: bool = False, push: bool = False, cross_compiling: bool = False,
                      platform: List[str] = ["linux/amd64", "linux/arm64", "linux/arm/v7"],
                      only_manifest: bool = False,
                      cwd: str = ".", use_sudo: bool = False, sudo_pwd: Optional[str] = None) -> None:
    cwdp = get_abs_path(cwd)
    if docker_register:
        docker_register = docker_register + "/"
    else:
        docker_register = ""
    image_name = f"{docker_register}{docker_register_namespace}/{project_name}"

    if cross_compiling is False:
        build_no_cross_compiling(
            cwdp=cwdp,
            dockerfile_name=dockerfile_name,
            image_name=image_name,
            version=version,
            as_latest_img=as_latest_img,
            push=push,
            use_sudo=use_sudo,
            sudo_pwd=sudo_pwd)
    else:
        if only_manifest:
            build_cross_compiling_only_manifest(
                cwdp=cwdp,
                dockerfile_name=dockerfile_name,
                image_name=image_name,
                version=version,
                platform=platform,
                as_latest_img=as_latest_img,
                use_sudo=use_sudo,
                sudo_pwd=sudo_pwd)
        else:
            build_cross_compiling(
                cwdp=cwdp,
                dockerfile_name=dockerfile_name,
                image_name=image_name,
                version=version,
                platform=platform,
                as_latest_img=as_latest_img,
                use_sudo=use_sudo,
                push=push,
                sudo_pwd=sudo_pwd)
