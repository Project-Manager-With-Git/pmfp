import warnings
from pathlib import Path
from typing import Optional, List
import yaml
from pmfp.utils.run_command_utils import run
from pmfp.entrypoint.docker_.compose.new.new_compose_dict import gen_compose
from pmfp.entrypoint.docker_.compose.new.save_compose import save_compose


def deploy_local(rebuild: bool,
                 cwdp: Path,
                 dockercompose_name: Optional[str] = None,
                 stack_name: Optional[str] = None,
                 compose_version: Optional[str] = None,
                 docker_register: Optional[str] = None,
                 docker_register_namespace: Optional[str] = None,
                 project_name: Optional[str] = None,
                 version: Optional[str] = None,
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
                 with_deploy_config: Optional[str] = None) -> None:
    """本地部署.

    Args:
        dockercompose_name (str): [description]
        rebuild (bool): [description]
        cwdp (Path): [description]
        stack_name (Optional[str], optional): [description]. Defaults to None.
    """
    if dockercompose_name:
        compose_path = cwdp.joinpath(dockercompose_name)
        if not compose_path.is_file():
            warnings.warn(f"compose file {compose_path} not find")
            return
        with open(compose_path, encoding="utf-8") as f:
            compose = yaml.load(f)
        composeversion = compose.get("version")
        if not composeversion:
            warnings.warn("compose file version not find")
            return
        if str(composeversion) == "2.4":
            print("deploy to stand-alone mode")
            cmd = f"sudo docker-compose -f {dockercompose_name} "
            if stack_name:
                cmd += f" -p {stack_name}"
            cmd += " up -d"
            if rebuild:
                cmd += " --build"
        elif str(composeversion) == "3.7" or str(composeversion) == "3.8":
            print("deploy to swarm mode")
            if not stack_name:
                warnings.warn("deploy compose to swarm must have stack_name")
                return
            cmd = f"sudo docker stack deploy --compose-file={dockercompose_name} {stack_name}"
        else:
            warnings.warn("unsupported compose version")
            return
        run(cmd, cwd=cwdp, visible=True, fail_exit=True)
    else:
        if project_name and compose_version and docker_register and docker_register_namespace and version:
            compose = gen_compose(compose_version=compose_version,
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
                                  with_deploy_config=with_deploy_config)
            save_compose(compose, cwdp)
            if compose_version == "2.4":
                print("deploy to stand-alone mode")
                cmd = "sudo docker-compose "
                if stack_name:
                    cmd += f" -p {stack_name}"
                cmd += " up -d"
                if rebuild:
                    cmd += " --build"
            elif compose_version == "3.7" or compose_version == "3.8":
                print("deploy to swarm mode")
                if not stack_name:
                    warnings.warn("deploy compose to swarm must have stack_name")
                    return
                cmd = f"sudo docker stack deploy {stack_name}"
            else:
                warnings.warn("unsupported compose version")
                return
            run(cmd, cwd=cwdp, visible=True, fail_exit=True)

        else:
            warnings.warn("should point out a project_name, compose_version, docker_register, docker_register_namespace, version for creating compose")
            return
