"""ppm docker compose deploy命令的处理."""
import warnings
from typing import Optional, List
from pmfp.utils.fs_utils import get_abs_path
from .core import dockercompose_deploy
from .deploy_local import deploy_local
from .deploy_portainer import deploy_portainer


@dockercompose_deploy.as_main
def deploy_dockercompose(portainer_url: Optional[str] = None,
                         portainer_username: Optional[str] = None,
                         portainer_password: Optional[str] = None,
                         deploy_endpoint: Optional[int] = None,
                         deploy_stack: Optional[int] = None,
                         stack_name: Optional[str] = None,
                         rebuild: bool = False,
                         update_version: bool = False,
                         dockercompose_name: Optional[str] = None,
                         docker_register: Optional[str] = None,
                         docker_register_namespace: Optional[str] = None,
                         project_name: Optional[str] = None,
                         version: Optional[str] = None,
                         updatemode: str = "level5",
                         compose_version: Optional[str] = None,
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
    if portainer_url:
        deploy_portainer(portainer_url=portainer_url,
                         cwdp=cwdp,
                         portainer_username=portainer_username,
                         portainer_password=portainer_password,
                         deploy_endpoint=deploy_endpoint,
                         deploy_stack=deploy_stack,
                         stack_name=stack_name,
                         update_version=update_version,
                         dockercompose_name=dockercompose_name,
                         docker_register=docker_register,
                         docker_register_namespace=docker_register_namespace,
                         project_name=project_name,
                         version=version,
                         updatemode=updatemode,
                         compose_version=compose_version,
                         command=command,
                         add_envs=add_envs,
                         use_host_network=use_host_network,
                         add_networks=add_networks,
                         add_extra_secrets=add_extra_secrets,
                         add_extra_configs=add_extra_configs,
                         add_volumes=add_volumes,
                         fluentd_url=fluentd_url,
                         extra_hosts=extra_hosts,
                         add_service=add_service,
                         with_deploy_config=with_deploy_config
                         )
    else:
        deploy_local(rebuild=rebuild,
                     cwdp=cwdp,
                     dockercompose_name=dockercompose_name,
                     stack_name=stack_name,
                     compose_version=compose_version,
                     docker_register=docker_register,
                     docker_register_namespace=docker_register_namespace,
                     project_name=project_name,
                     version=version,
                     command=command,
                     add_envs=add_envs,
                     use_host_network=use_host_network,
                     add_networks=add_networks,
                     add_extra_secrets=add_extra_secrets,
                     add_extra_configs=add_extra_configs,
                     add_volumes=add_volumes,
                     fluentd_url=fluentd_url,
                     extra_hosts=extra_hosts,
                     add_service=add_service,
                     with_deploy_config=with_deploy_config)
