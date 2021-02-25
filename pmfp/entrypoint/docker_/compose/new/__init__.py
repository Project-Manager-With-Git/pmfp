import warnings
import time
from typing import Optional, List
import yaml
import pyaml
from pmfp.utils.fs_utils import get_abs_path
from .core import dockercompose_new
from .new_compose import new_compose


@dockercompose_new.as_main
def new_dockercompose(
        compose_version: str,
        dockercompose_name: str = "docker-compose.yml",
        dockerfile_dir: Optional[str] = None, dockerfile_name: Optional[str] = None,
        docker_register: Optional[str] = None, docker_register_namespace: Optional[str] = None,
        project_name: Optional[str] = None, version: Optional[str] = None,
        nfs_addr: Optional[str] = None, nfs_shared_path: str = "/", use_nfs_v4: bool = False,
        language: Optional[str] = None, extend: bool = False,
        fluentd_url: Optional[str] = None,
        extra_hosts: Optional[List[str]] = None, use_host_network: bool = False, ports: Optional[List[str]] = None,
        add_service: Optional[List[str]] = None, cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
    docker_composep = cwdp.joinpath(dockercompose_name)
    if docker_composep.exists():
        with open(docker_composep, encoding="utf-8") as f:
            StackFileContent = f.read()
        now = int(time.time())
        docker_composep_bak = cwdp.joinpath(f"{dockercompose_name}.{now}_bak")
        with open(docker_composep_bak, "w", newline="", encoding="utf-8") as f:
            f.write(StackFileContent)
        new_compose(compose_version=compose_version,
                    dockercompose_name=dockercompose_name,
                    dockerfile_dir=dockerfile_dir,
                    dockerfile_name=dockerfile_name,
                    docker_register=docker_register,
                    docker_register_namespace=docker_register_namespace,
                    project_name=project_name,
                    version=version,
                    nfs_addr=nfs_addr,
                    nfs_shared_path=nfs_shared_path,
                    use_nfs_v4=use_nfs_v4,
                    language=language,
                    extend=extend,
                    fluentd_url=fluentd_url,
                    extra_hosts=extra_hosts,
                    use_host_network=use_host_network,
                    ports=ports,
                    add_service=add_service,
                    cwdp=cwdp)
    else:
        new_compose(compose_version=compose_version,
                    dockercompose_name=dockercompose_name,
                    dockerfile_dir=dockerfile_dir,
                    dockerfile_name=dockerfile_name,
                    docker_register=docker_register,
                    docker_register_namespace=docker_register_namespace,
                    project_name=project_name,
                    version=version,
                    nfs_addr=nfs_addr,
                    nfs_shared_path=nfs_shared_path,
                    use_nfs_v4=use_nfs_v4,
                    language=language,
                    extend=extend,
                    fluentd_url=fluentd_url,
                    extra_hosts=extra_hosts,
                    use_host_network=use_host_network,
                    ports=ports,
                    add_service=add_service,
                    cwdp=cwdp)
