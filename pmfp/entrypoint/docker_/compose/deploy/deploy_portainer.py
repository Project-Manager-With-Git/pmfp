import warnings
import json
from pathlib import Path
from typing import Optional, Dict, List
from mypy_extensions import TypedDict

import yaml
import requests as rq
from pmfp.const import PMFP_CONFIG_DEFAULT_NAME
from pmfp.entrypoint.docker_.compose.new.merge_compose_dict import merge_compose
from pmfp.entrypoint.docker_.compose.new.save_compose import compose_dict_to_str, save_compose
from pmfp.entrypoint.docker_.compose.new.new_compose_dict import gen_compose
from pmfp.entrypoint.docker_.compose.new.typedef import (
    ServiceSchema,
    ServicesSchema,
    ComposeSchema
)


def get_jwt(portainer_url: str, portainer_username: str, portainer_password: str) -> str:
    """登录portainer获取行动权限.

    Args:
        portainer_url (str): portainer的地址
        portainer_username (str): 登录用户名
        portainer_password (str): 登录密码

    Returns:
        str: jwt令牌
    """
    res = rq.post(portainer_url + "/api/auth", json={"Username": portainer_username, "Password": portainer_password})
    if res.status_code != 200:
        raise AttributeError(f"get jwt error with code {res.status_code}")
    jwt = res.json().get("jwt")
    return jwt


def get_target_stack(portainer_url: str, jwt: str, deploy_stack: int) -> ComposeSchema:
    """获取目标stack用于更新.

    Args:
        portainer_url (str): portainer的地址
        jwt (str): jwt令牌
        deploy_stack (int): 要获取的stack id

    Returns:
        ComposeSchema: 旧stack的compose内容字典
    """
    res = rq.post(
        portainer_url + f"/api/stacks/{deploy_stack}/file",
        headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt})
    )
    if res.status_code != 200:
        raise AttributeError(f"get target stack {deploy_stack} error with code {res.status_code}")
    StackFileContent = res.json().get("StackFileContent")
    s = yaml.load(StackFileContent)
    return s


EndpointInfoSchema = TypedDict("EndpointInfoSchema", {
    "type": int,
    "swarmID": str
}, total=False)


def get_endpoints_info(portainer_url: str, jwt: str, deploy_endpoint: int) -> EndpointInfoSchema:
    """获取端点信息

    Args:
        portainer_url (str): portainer的地址
        jwt (str): jwt令牌
        deploy_endpoint (int): 端点id

    Raises:
        AttributeError: 请求失败

    Returns:
        EndpointInfoSchema: `type`为端点类型,1为stand-alone,2为swarm;`swarmID`为swarm节点的集群id
    """
    res = rq.post(
        portainer_url + f"/api/endpoints/{deploy_endpoint}",
        headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt})
    )
    if res.status_code != 200:
        raise AttributeError(f"get endpoint {deploy_endpoint} info error with code {res.status_code}")
    Type = res.json().get("Type")
    result: EndpointInfoSchema = {
        "type": int(Type)
    }
    if Type == 2:
        res1 = rq.get(
            portainer_url + f"/api/endpoints/{deploy_endpoint}/docker/swarm",
            headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt})
        )
        if res1.status_code != 200:
            raise AttributeError("get endpoint swarn info error")
        result.update({"swarmID": res1.json().get("ID")})
    return result


def create_stack(portainer_url: str,
                 jwt: str,
                 deploy_endpoint: int,
                 compose: ComposeSchema,
                 cwdp: Path,
                 stack_name:
                 Optional[str] = None,
                 swarmID: Optional[str] = None) -> None:
    """在没有指定部署stack的情况下创建一个stack.

    Args:
        portainer_url (str): portainer的地址
        jwt (str): jwt令牌
        deploy_endpoint (int): 端点id
        compose (ComposeSchema): 要部署的stack的compose字典
        cwdp (Path): 本地执行位置
        stack_name (Optional[str], optional): 部署的stack名. Defaults to None.
        swarmID (Optional[str], optional): swarm模式的集群id. Defaults to None.

    Raises:
        AttributeError: [description]
        AttributeError: [description]
        AttributeError: [description]
    """
    if not stack_name:
        raise AttributeError("stack name can not empty")
    compose_str = compose_dict_to_str(compose)
    if compose["version"] == 2.4:
        task_type = 2
        query_json = {
            "env": [
            ],
            "name": stack_name,
            "stackFileContent": compose_str
        }
    else:
        if not swarmID:
            raise AttributeError("deploy new stack need swarmID")
        task_type = 1
        query_json = {
            "env": [],
            "name": stack_name,
            "stackFileContent": compose_str,
            "swarmID": swarmID
        }

    res = rq.post(
        portainer_url + "/api/stacks",
        headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
        params={
            "method": "string",
            "type": task_type,
            "endpointId": int(deploy_endpoint)
        },
        json=query_json)
    if res.status_code != 200:
        raise AttributeError(f"deploy stack error with code {res.status_code}")
    deploy_stack = res.json().get("Id")
    # 保存deploy_stackid
    ppmrc = cwdp.joinpath(PMFP_CONFIG_DEFAULT_NAME)
    content: Dict[str, int] = {
        "deploy_stack": deploy_stack
    }
    if ppmrc.exists():
        with open(ppmrc) as f:
            old = json.load(f)
        with open(ppmrc, "w", encoding="utf-8") as f:
            old.update(**content)
            json.dump(old, f, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        with open(ppmrc, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4, sort_keys=True)


def update_image_version(docker_register: str,
                         docker_register_namespace: str,
                         project_name: str,
                         version: str,
                         deploy_endpoint: int,
                         deploy_stack: int,
                         portainer_url: str,
                         jwt: str) -> None:
    """只更新旧compose中image的版本.

    Args:
        docker_register (str): 镜像仓库url
        docker_register_namespace (str): 在镜像仓库中的命名空间
        project_name (str): 项目名,也就是镜像名
        version (str): 当前版本
        deploy_endpoint (int): 部署的端点
        deploy_stack (int): 部署的stack
        portainer_url (str): 部署的portainer位置
        jwt (str): 部署的令牌

    Raises:
        AttributeError: 请求失败
    """
    old_compose = get_target_stack(portainer_url, jwt, deploy_stack)
    image_without_version_str = f"{docker_register}/{docker_register_namespace}/{project_name}"
    image_str = f"{image_without_version_str}:{version}"

    services: ServicesSchema = old_compose["services"]
    for _, info in services.items():
        image = info["image"]
        if image_without_version_str in image:
            info["image"] = image_str
    res = rq.put(
        f"{portainer_url}/stacks/{deploy_stack}",
        headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
        params={"endpointId": deploy_endpoint},
        json={
            "StackFileContent": old_compose,
            "Prune": False
        }
    )
    if res.status_code != 200:
        raise AttributeError("get endpoint swarn info error")
    print(f"update version for image {image_str}")
    print(res.json())


def update_satck(compose: ComposeSchema,
                 deploy_endpoint: int,
                 deploy_stack: int,
                 portainer_url: str,
                 jwt: str) -> None:
    res = rq.put(
        f"{portainer_url}/stacks/{deploy_stack}",
        headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
        params={"endpointId": deploy_endpoint},
        json={
            "StackFileContent": compose,
            "Prune": False
        }
    )
    if res.status_code != 200:
        raise AttributeError("get endpoint swarn info error")
    print("update stack with mode ok")
    print(res.json())


def deploy_portainer(portainer_url: str,
                     cwdp: Path,
                     portainer_username: Optional[str] = None,
                     portainer_password: Optional[str] = None,
                     deploy_endpoint: Optional[int] = None,
                     deploy_stack: Optional[int] = None,
                     stack_name: Optional[str] = None,
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
                     with_deploy_config: Optional[str] = None) -> None:
    """远程部署到portainer.
    如果制定了`dockercompose_name`则:
    1. 如果没有指定`deploy_stack`则根据本地docker-compose文件创建stack
    2. 如果指定了`deploy_stack`则使用本地docker-compose文件融合已有的stack(默认level5方式融合)更新stack

    如果没有指定dockercompose_name则:
    1. 指定了`update_version`则只更新原始stack中的镜像版本
    2. 没有指定`update_version`,则:
        1. 如果没有指定`deploy_stack`则根据命令行指示创建stack并在本地保存,然后创建到portainer中
        2. 如果指定了`deploy_stack`则根据命令行指示创建stack并与已有的融合(默认level5方式融合)然后保存到本地并更新stack

    """
    if not deploy_endpoint:
        warnings.warn("deploy to portainer need to point out the endpoint")
        return
    if not portainer_username or not portainer_password:
        warnings.warn("deploy to portainer need to point out the username and password")
        return

    jwt = get_jwt(portainer_url, portainer_username, portainer_password)
    try:
        endpoint_info = get_endpoints_info(portainer_url, jwt, deploy_endpoint)
    except Exception as e:
        warnings.warn(str(e))
        return
    else:
        # 分支1
        if dockercompose_name:
            compose_path = cwdp.joinpath(dockercompose_name)
            if not compose_path.is_file():
                warnings.warn(f"compose file {compose_path} not find")
                return
            with open(compose_path, encoding="utf-8") as f:
                compose = yaml.load(f)

            version = compose.get("version")
            if not version:
                warnings.warn("compose file version not find")
                return
            if endpoint_info["type"] == 1 and version != "2.4":
                warnings.warn("compose file version must 2.4 to deploy in stand-alone mode")
                return
            if endpoint_info["type"] == 2 and version not in ("3.7", "3.8"):
                warnings.warn("compose file version must 3.7 or 3.8 to deploy in swarm mode")
                return
            # 分支1.1
            if not deploy_stack:
                # 新建stack
                create_stack(portainer_url, jwt, deploy_endpoint, compose, cwdp, stack_name, swarmID=endpoint_info.get("swarmID"))
                return
            # 分支1.2
            else:
                # 更新已有的stack
                if not project_name:
                    warnings.warn("update stack need to point out project_name")
                    return
                old_compose = get_target_stack(portainer_url, jwt, deploy_stack)
                merged_compose = merge_compose(old=old_compose, new=compose, project_name=project_name, updatemode=updatemode)
                update_satck(merged_compose,
                             deploy_endpoint,
                             deploy_stack,
                             portainer_url,
                             jwt)
                return
        # 分支2
        else:
            # 如果本地没有指定dockercompose_name
            # 分支2.1
            if update_version:
                if deploy_endpoint and deploy_stack and project_name and version and docker_register and docker_register_namespace:
                    update_image_version(docker_register,
                                         docker_register_namespace,
                                         project_name,
                                         version,
                                         deploy_endpoint,
                                         deploy_stack,
                                         portainer_url,
                                         jwt)
                    return
                else:
                    warnings.warn("should point out a dockercompose name")
                    return
            # 分支2.2
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
                    # 分支2.2.1
                    if not deploy_stack:
                        save_compose(compose, cwdp)
                        create_stack(portainer_url, jwt, deploy_endpoint, compose, cwdp, stack_name, swarmID=endpoint_info.get("swarmID"))
                        return
                    # 分支2.2.2
                    else:
                        # 更新已有的stack
                        if not project_name:
                            warnings.warn("update stack need to point out project_name")
                            return
                        old_compose = get_target_stack(portainer_url, jwt, deploy_stack)
                        merged_compose = merge_compose(old=old_compose, new=compose, project_name=project_name, updatemode=updatemode)
                        update_satck(
                            merged_compose,
                            deploy_endpoint,
                            deploy_stack,
                            portainer_url,
                            jwt)
                        return
                else:
                    warnings.warn("should point out a project_name, compose_version, docker_register, docker_register_namespace, version for creating compose")
                    return
