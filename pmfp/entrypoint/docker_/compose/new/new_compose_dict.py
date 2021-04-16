import warnings
from typing import Dict, Any, List, Union, Optional, Collection, Mapping


def gen_default_log_compose(fluentd_url: Optional[str] = None) -> Dict[str, Union[str, Dict[str, str]]]:
    """构造一级字段`x-log`默认的log配置.

    Args:
        fluentd_url (Optional[str], optional): 如果设置了fluentd_url则使用fluennted维护log. Defaults to None.

    Returns:
        Dict[str, Union[str, Dict[str, str]]]: 外部的全局log配置字段x-log的内容
    """
    default_log: Dict[str, Union[str, Dict[str, str]]] = {
        "driver": "json-file",
        "options": {
            "max-siz": "10m",
            "max-file": "3"
        }
    }
    if fluentd_url:
        default_log = {
            "driver": "fluentd",
            "options": {
                "fluentd-address": "fluentd_url"
            }
        }
    return default_log


def gen_default_extra_hosts_compose(extra_hosts: List[str]) -> Dict[str, List[str]]:
    """构造一级字段`x-extra_hosts`默认的域名映射.

    Args:
        extra_hosts (List[str]): 映射列表

    Returns:
        Dict[str, List[str]]: 外部的全局域名映射字段x-extra_hosts的内容
    """
    return {
        "extra_hosts": extra_hosts
    }


def gen_volume_compose(add_volumes: List[str]) -> Dict[str, Optional[Dict[str, Union[bool, str, Dict[str, str]]]]]:
    """生成一级字段`volumes`的配置.

    形式可以有3种:
    <volume_name>::<path>;会在volumes种构造内部`volume_name`并挂载到服务的path目录
    <volume_name>$$extra::<path>;会在volumes种构造外部`volume_name`并挂载到服务的path目录
    <volume_name>$$path::<path>;直接挂载local路径到服务的path目录
    <volume_name>$$nfs@<nfs_addr>@<nfs_shared_path>@<nfs_opts>::<path>;挂载nfs到服务的path目录

    Args:
        add_volumes (List[str]): 添加挂载的配置字符串

    Returns:
        Dict[str, Optional[Dict[str, Union[bool, str, Dict[str, str]]]]]: volumes字段的配置字典
    """
    result: Dict[str, Optional[Dict[str, Union[bool, str, Dict[str, str]]]]] = {}
    for volume_conf in add_volumes:
        try:
            volume_info, _ = volume_conf.split("::")
        except Exception:
            warnings.warn(f"skip volumes config {volume_conf}, something is wrong")
            continue
        else:
            if volume_info.endswith("$$extra"):
                volume_name = volume_info.replace("$$extra", "")
                result[volume_name] = {
                    "external": True
                }
            elif volume_info.endswith("$$path"):
                continue
            elif "$$nfs@" in volume_info:
                try:
                    volume_name, confs = volume_info.split("$$nfs@")
                except Exception:
                    warnings.warn(f"skip nfs volumes config {volume_conf}, something is wrong")
                    continue
                else:
                    try:
                        nfs_addr, nfs_shared_path, nfs_opts = confs.split("@")
                    except Exception:
                        warnings.warn(f"skip nfs volumes config {volume_conf}, something is wrong")
                        continue
                    else:
                        result[volume_name] = {
                            "driver_opts": {
                                "type": "nfs",
                                "o": f"addr={nfs_addr},{nfs_opts}",
                                "device": nfs_shared_path
                            }
                        }
            else:
                result[volume_info] = None
    return result


def gen_network_compose(compose_version: str, use_host_network: bool,
                        add_networks: List[str]) -> Dict[str, Optional[Dict[str, Union[bool, str]]]]:
    """生成一级字段`networks`的配置.

    添加网络可以有如下两种形式:
    + <network_name>添加内部网络
    + <network_name>$$extra添加外部网络

    如果使用的compose版本为3.7或者3.8,且使用宿主机网路,则还会添加一个`myhostnetwork`用于表示宿主机网络

    Args:
        compose_version (str): 使用的compose版本
        use_host_network (bool): 是否使用宿主机网络
        add_networks (List[str]): 添加网络的配置字符串

    Returns:
        Dict[str, Optional[Dict[str, Union[bool, str]]]]: networks字段的配置字典
    """
    result: Dict[str, Optional[Dict[str, Union[bool, str]]]] = {}
    if use_host_network is True and compose_version in ("3.7", "3.8"):
        result["myhostnetwork"] = {
            "external": True,
            "name": "host"
        }
    for network in add_networks:
        if network.endswith("$$extra"):
            network_name = network.replace("$$extra", "")
            result[network_name] = {
                "external": True
            }
        else:
            result[network] = None
    return result


def gen_config_compose(add_extra_configs: List[str]) -> Dict[str, Dict[str, bool]]:
    """生成一级字段`configs`的配置.

    Args:
        add_extra_configs (List[str]): 添加配置项的配置字符串

    Returns:
        Dict[str, Dict[str, bool]]: configs字段的配置字典
    """
    result: Dict[str, Dict[str, bool]] = {}
    for conf in add_extra_configs:
        result[conf] = {
            "external": True
        }
    return result


def gen_secret_compose(add_extra_secrets: List[str]) -> Dict[str, Dict[str, bool]]:
    """生成一级字段`secrets`的配置.

    Args:
        add_extra_secrets (List[str]): 添加密码项的配置字符串

    Returns:
        Dict[str, Dict[str, bool]]: secret字段的配置字典
    """
    result: Dict[str, Dict[str, bool]] = {}
    for secret in add_extra_secrets:
        result[secret] = {
            "external": True
        }
    return result


def gen_thirdpart_service_compose(service_name: str) -> Mapping[Optional[str], Dict[str, Union[str, Dict[str, Any], List[str]]]]:
    """为第三方服务构造compose.

    Args:
        service_name (str): 要生成的服务名

    Raises:
        AttributeError: 不支持的第三方服务名

    Returns:
        Dict[str, Dict[str, Any]]: compose配置的字典
    """
    result: Mapping[Optional[str], Dict[str, Union[str, Dict[str, Any], List[str]]]] = {}
    if service_name == "redis":
        result["redis"] = {
            "image": "redis:latest",
            "mem_limit": "500m",
            "restart": "on-failure",
            "ports": ["6379:6379"]
        }
    elif service_name == "postgres":
        result["postgres"] = {
                "image": "timescale/timescaledb-postgis:latest-pg13",
                "mem_limit": "500m",
                "restart": "on-failure",
                "ports": ["5432:5432"],
                "environment": {
                    "POSTGRES_PASSWORD": "postgres"
                },
                "volumes": [
                    "postgres_data:/var/lib/postgresql/data"
                ],
                "command": ["-c", "max_connections=300"]
            }
        }
    elif service_name == "zookeeper":
        result = {}
        for i in range(1, 4):
            zookeeper_sers: Dict[str, Union[str, List[str], Dict[str, str]]] = {
                "image": "zookeeper",
                "hostname": f"zoo{i}",
                "ports": ["2181:2181"],
                "mem_limit": "500m",
                "restart": "on-failure",
                "environment": {
                    "ZOO_MY_ID": str(i),
                    "ZOO_SERVERS": "server.1=0.0.0.0:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181"
                }
            }
            result.update(
                {
                    f"zoo{i}": zookeeper_sers
                }
            )
        return result
    elif service_name == "envoy":
        return {
            "envoy": {
                "image": "envoyproxy/envoy-dev:76286f6152666c73d9379f21f43152bd03b00f78",
                "hostname": f"zoo{i}",
                "ports": ["10000:10000"],
                "mem_limit": "500m",
                "restart": "on-failure",
                "volumes": ["./envoy.yaml:/etc/envoy/envoy.yaml"]
            }
        }
    else:
        raise AttributeError("unsupport service_name")


def gen_project_service_compose(compose_version: str,
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
                                default_extra_hosts: Optional[Dict[str, List[str]]] = None,
                                default_log: Optional[Dict[str, Union[str, Dict[str, str]]]] = None
                                ) -> Dict[str, Union[str, Dict[str, Any], List[str]]]:
    """生成项目本身的service项.

    Args:
        compose_version (str): docker compose版本
        dockerfile_dir (Optional[str], optional): dockerfile的存放目录. Defaults to None.
        dockerfile_name (Optional[str], optional): dockerfile名. Defaults to None.
        docker_register (Optional[str], optional): 镜像库地址. Defaults to None.
        docker_register_namespace (Optional[str], optional): 项目在镜像仓库的命名空间. Defaults to None.
        project_name (Optional[str], optional): 项目名. Defaults to None.
        version (Optional[str], optional): 项目版本,也是镜像版本,不填会使用latest. Defaults to None.
        command (Optional[str], optional): 执行命令. Defaults to None.
        add_envs (Optional[List[str]], optional): 环境变量. Defaults to None.
        use_host_network (bool, optional): 是否使用宿主机网络. Defaults to False.
        ports (Optional[List[str]], optional): 端口映射. Defaults to None.
        add_networks (Optional[List[str]], optional): 使用网络. Defaults to None.
        add_extra_secrets (Optional[List[str]], optional): 使用的密码. Defaults to None.
        add_extra_configs (Optional[List[str]], optional): 使用的配置. Defaults to None.
        add_volumes (Optional[List[str]], optional): 使用的挂载. Defaults to None.
        default_extra_hosts (Optional[Dict[str, List[str]]], optional): 域名映射. Defaults to None.
        default_log (Optional[Dict[str, Dict[str, Union[str, Dict[str, str]]]]], optional): log配置. Defaults to None.

    Raises:
        AttributeError: compose版本不支持

    Returns:
        Dict[str, Union[str, Dict[str, Any], List[str]]]: 项目自身的compose项
    """
    project_serv: Dict[str, Union[str, Dict[str, Any], List[str]]] = {}
    # build and image
    if docker_register_namespace and project_name:
        docker_register = docker_register + "/" if docker_register else ""
        img_version = f":{version}" if version else "latest"
        project_serv.update({
            "image": f"{docker_register}{docker_register_namespace}/{project_name}{img_version}",
        })
    else:
        if dockerfile_dir is None:
            dockerfile_dir = "."
    if dockerfile_dir:
        build_block = {
            "context": dockerfile_dir
        }
        if dockerfile_name:
            build_block.update({
                "dockerfile": dockerfile_name

            })
        project_serv.update({
            "build": build_block
        })
    # set logging
    if default_log:
        project_serv.update({
            "logging": {
                "<<": default_log
            },
        })

    # network
    networks: List[str] = []
    if add_networks:
        for network in add_networks:
            if network.endswith("$$extra"):
                network_name = network.replace("$$extra", "")
                networks.append(network_name)
            else:
                networks.append(network)
    if compose_version == "2.4":
        # 2.4 special
        # network
        if use_host_network:
            project_serv.update({
                "network_mode": "host"
            })
        else:
            if ports:
                project_serv.update({
                    "ports": ports
                })
            if len(networks) > 0:
                project_serv.update({
                    "networks": networks
                })

    elif compose_version in ("3.7", "3.8"):
        if use_host_network:
            networks = ["myhostnetwork"]
        else:
            if ports:
                project_serv.update({
                    "ports": ports
                })
        if len(networks) > 0:
            project_serv.update({
                "networks": networks
            })
    else:
        raise AttributeError(f"unsupport compose_version {compose_version}")

    if default_extra_hosts:
        project_serv.update({
            "<<": default_extra_hosts
        })

    # volumes
    volumes: List[str] = []
    if add_volumes:
        for volume_conf in add_volumes:
            try:
                volume_info, bind_path = volume_conf.split("::")
            except Exception:
                warnings.warn(f"skip volumes config {volume_conf}, something is wrong")
                continue
            else:
                if volume_info.endswith("$$extra"):
                    volume_name = volume_info.replace("$$extra", "")
                elif volume_info.endswith("$$path"):
                    volume_name = volume_info.replace("$$path", "")
                elif "$$nfs@" in volume_info:
                    try:
                        volume_name, _ = volume_info.split("$$nfs@")
                    except Exception:
                        warnings.warn(f"skip nfs volumes config {volume_conf}, something is wrong")
                        continue

                else:
                    volume_name = volume_info
                volumes.append(f"{volume_name}:{bind_path}")
    if len(volumes) > 0:
        project_serv.update({
            "volumes": volumes
        })
    # config&secrets
    if compose_version in ("3.7", "3.8"):
        # config
        configs: List[str] = []
        if add_extra_configs:
            for conf in add_extra_configs:
                configs.append(conf)
        if len(configs) > 0:
            project_serv.update({
                "configs": configs
            })

        # secrets
        secrets: List[str] = []
        if add_extra_secrets:
            for secret in add_extra_secrets:
                secrets.append(secret)
        if len(secrets) > 0:
            project_serv.update({
                "secrets": secrets
            })
    else:
        warnings.warn(f"{compose_version} 不支持 configs 和 secrets")

    # env
    if add_envs:
        environments: Dict[str, str] = {}
        for i in add_envs:
            try:
                k, v = i.split(":")
            except Exception:
                warnings.warn(f"skip env config {i}, something is wrong")
                continue
            else:
                environments[k] = v
        if len(environments) > 0:
            project_serv.update({
                "environment": environments
            })

    # cmd
    if command:
        if command.startswith("[") and command.endswith("]"):
            try:
                command_list = eval(command)
            except SyntaxError:
                warnings.warn(f"skip cmd {command}, SyntaxError")
            except Exception:
                warnings.warn(f"skip cmd {command}, something is wrong")
            else:
                project_serv.update({
                    "command": command_list
                })
        else:
            project_serv.update({
                "command": command
            })

    # deploy
    if compose_version == "2.4":
        project_serv.update({
            "cpus": "0.5",
            "mem_limit": "256m",
            "mem_reservation": "64m",
            "restart": "on-failure",
        })

    elif compose_version == "3.7":
        project_serv.update({
            "deploy": {
                "mode": "global",
                "resources": {
                    "limits": {
                        "cpus": "1.0",
                        "memory": "400M"
                    },
                    "reservations": {
                        "cpus": "0.25",
                        "memory": "20M"
                    }
                },
                "restart_policy": {
                    "condition": "on-failure",
                    "delay": "5s",
                    "max_attempts": 3,
                    "window": "100s"
                },
                "placement": {
                    "constraints": ["node.role==manager"],
                    "preferences": ["spread: node.labels.zone"]
                },
                "update_config": {
                    "parallelism": 2,
                    "delay": "10s",
                    "order": "stop-first",
                    "failure_action": "rollback"
                },
                "rollback_config": {
                    "parallelism": 2,
                    "delay": "2s",
                    "order": "stop-first",
                }
            }
        })
    elif compose_version == "3.8":
        project_serv.update({
            "deploy": {
                "mode": "replicated",
                "replicas": 6,
                "resources": {
                    "limits": {
                        "cpus": "1.0",
                        "memory": "400M"
                    },
                    "reservations": {
                        "cpus": "0.25",
                        "memory": "20M"
                    }
                },
                "restart_policy": {
                    "condition": "on-failure",
                    "delay": "5s",
                    "max_attempts": 3,
                    "window": "100s"
                },
                "placement": {
                    "constraints": ["node.role==manager", "engine.labels.operatingsystem==ubuntu 18.04"],
                    "preferences": ["spread: node.labels.zone"],
                    "max_replicas_per_node": 1
                },
                "update_config": {
                    "parallelism": 2,
                    "delay": "10s",
                    "order": "stop-first",
                    "failure_action": "rollback"
                },
                "rollback_config": {
                    "parallelism": 2,
                    "delay": "2s",
                    "order": "stop-first",
                }
            }
        })
    else:
        raise AttributeError(f"unsupport compose_version {compose_version}")

    return project_serv


def gen_compose(compose_version: str,
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
                add_service: Optional[List[str]] = None
                ):
    """生成compose字典.

    Args:
        compose_version (str): docker compose版本
        dockerfile_dir (Optional[str], optional): dockerfile的存放目录. Defaults to None.
        dockerfile_name (Optional[str], optional): dockerfile名. Defaults to None.
        docker_register (Optional[str], optional): 镜像库地址. Defaults to None.
        docker_register_namespace (Optional[str], optional): 项目在镜像仓库的命名空间. Defaults to None.
        project_name (Optional[str], optional): 项目名. Defaults to None.
        version (Optional[str], optional): 项目版本,也是镜像版本,不填会使用latest. Defaults to None.
        command (Optional[str], optional): 执行命令. Defaults to None.
        add_envs (Optional[List[str]], optional): 环境变量. Defaults to None.
        use_host_network (bool, optional): 是否使用宿主机网络. Defaults to False.
        ports (Optional[List[str]], optional): 端口映射. Defaults to None.
        add_networks (Optional[List[str]], optional): 使用网络. Defaults to None.
        add_extra_secrets (Optional[List[str]], optional): 使用的密码. Defaults to None.
        add_extra_configs (Optional[List[str]], optional): 使用的配置. Defaults to None.
        add_volumes (Optional[List[str]], optional): 使用的挂载. Defaults to None.
        default_extra_hosts (Optional[Dict[str, List[str]]], optional): 域名映射. Defaults to None.
        default_log (Optional[Dict[str, Dict[str, Union[str, Dict[str, str]]]]], optional): log配置. Defaults to None.
    """
    default_log = gen_default_log_compose(fluentd_url)
    compose = {
        "version": f'"{compose_version}"',
        "x-log": default_log,
        "default_log": default_log,
    }
    default_extra_hosts = None
    if extra_hosts:
        default_extra_hosts = gen_default_extra_hosts_compose(extra_hosts)
        compose.update({
            "x-extra_hosts": default_extra_hosts,
            "default_extra_hosts": default_extra_hosts,
        })
    services = {}
    project_service = gen_project_service_compose(compose_version=compose_version,
                                                  dockerfile_dir=dockerfile_dir, dockerfile_name=dockerfile_name,
                                                  docker_register=docker_register, docker_register_namespace=docker_register_namespace,
                                                  project_name=project_name, version=version,
                                                  command=command,
                                                  add_envs=add_envs,
                                                  use_host_network=use_host_network, ports=ports,
                                                  add_networks=add_networks,
                                                  add_extra_secrets=add_extra_secrets,
                                                  add_extra_configs=add_extra_configs,
                                                  add_volumes=add_volumes, default_extra_hosts=default_extra_hosts,
                                                  default_log=default_log)
    services[project_name] = project_service
    if add_service:
        for service_name in add_service:

            services.update(gen_thirdpart_service_compose(service_name))
