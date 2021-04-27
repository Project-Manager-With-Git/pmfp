"""ppm docker compose new命令的处理."""
import warnings
import time
from typing import Optional, List
import yaml
from pmfp.utils.fs_utils import get_abs_path
from .core import dockercompose_new

from .new_compose_dict import gen_compose
from .merge_compose_dict import merge_compose
from .save_compose import save_compose


@dockercompose_new.as_main
def new_dockercompose(
        compose_version: str,
        dockercompose_name: str = "docker-compose.yml",
        updatemode: str = "level5",
        dockerfile_dir: Optional[str] = None, dockerfile_name: Optional[str] = None,
        docker_register: Optional[str] = None, docker_register_namespace: Optional[str] = None,
        project_name: Optional[str] = None, version: Optional[str] = None,
        command: Optional[str] = None,
        add_envs: Optional[List[str]] = None,
        use_host_network: bool = False, ports: Optional[List[str]] = None,
        add_networks: Optional[List[str]] = None,
        add_extra_secrets: Optional[List[str]] = None,
        add_extra_configs: Optional[List[str]] = None,
        add_volumes: Optional[List[str]] = None,
        fluentd_url: Optional[str] = None,
        extra_hosts: Optional[List[str]] = None,
        add_service: Optional[List[str]] = None,
        with_deploy_config: Optional[str] = None,
        cwd: str = ".") -> None:

    cwdp = get_abs_path(cwd)
    docker_composep = cwdp.joinpath(dockercompose_name)
    new_compose = gen_compose(
        compose_version=compose_version,
        dockerfile_dir=dockerfile_dir,
        dockerfile_name=dockerfile_name,
        docker_register=docker_register,
        docker_register_namespace=docker_register_namespace,
        project_name=project_name,
        version=version,
        command=command,
        add_envs=add_envs,
        use_host_network=use_host_network,
        ports=ports,
        add_networks=add_networks,
        add_extra_secrets=add_extra_secrets,
        add_extra_configs=add_extra_configs,
        add_volumes=add_volumes,
        fluentd_url=fluentd_url,
        extra_hosts=extra_hosts,
        add_service=add_service,
        with_deploy_config=with_deploy_config
    )
    if docker_composep.exists():
        # 如果指定名字的compose文件已经存在,则执行更新操作
        with open(docker_composep, encoding="utf-8") as f:
            StackFileContent = f.read()
        # 保存留档
        now = int(time.time())
        docker_composep_bak = cwdp.joinpath(f"{dockercompose_name}.{now}_bak")
        with open(docker_composep_bak, "w", newline="", encoding="utf-8") as f:
            f.write(StackFileContent)
        # 执行更新
        if not project_name:
            project_name = "app"
        merged_compose = merge_compose(old=yaml.load(StackFileContent), new=new_compose, project_name=project_name, updatemode=updatemode)
        save_compose(compose=merged_compose, cwdp=cwdp, dockercompose_name=dockercompose_name)
    else:
        # 如果指定名字的compose文件不存在,则执行创建操作
        save_compose(compose=new_compose, cwdp=cwdp, dockercompose_name=dockercompose_name)
