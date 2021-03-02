import warnings
from pathlib import Path
from typing import Optional, List
import pyaml


def new_compose(
        compose_version: str, cwdp: Path,
        dockercompose_name: str = "docker-compose.yml",
        dockerfile_dir: Optional[str] = None, dockerfile_name: Optional[str] = None,
        docker_register: Optional[str] = None, docker_register_namespace: Optional[str] = None,
        project_name: Optional[str] = None, version: Optional[str] = None,
        nfs_addr: Optional[str] = None, nfs_shared_path: str = "/", use_nfs_v4: bool = False,
        language: Optional[str] = None, extend: bool = False,
        fluentd_url: Optional[str] = None,
        extra_hosts: Optional[List[str]] = None, use_host_network: bool = False, ports: Optional[List[str]] = None,
        add_service: Optional[List[str]] = None) -> None:

    # default_log
    default_log = {
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

    compose = {
        "version": f'"{compose_version}"',
        "x-log": default_log,
        "default_log": default_log,
    }
    services = {
        "init": True
    }
    project_serv = {}
    # build and image
    if docker_register_namespace and project_name:
        docker_register = docker_register + "/" if docker_register else ""
        img_version = f":{version}" if version else ""
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
    project_serv.update({
        "logging": {
            "<<": default_log
        },
    })
    # extra_hosts
    if extra_hosts:
        default_extra_hosts = {
            "extra_hosts": extra_hosts
        }
        compose.update({
            "x-extra_hosts": default_extra_hosts,
            "default_extra_hosts": default_extra_hosts,
        })
        project_serv.update({
            "<<": default_extra_hosts
        })

    # environment
    if project_name:
        example_env = project_name.upper() + "_LOG_LEVEL"
        project_serv.update({
            "environment": {
                example_env: "DEBUG"
            }
        })

    # command
    if language == "cython" or (language == "py" and extend is True):
        project_serv.update({
            "command": ["python", "app"]
        })

    if language == "py" and extend is False:
        project_serv.update({
            "command": ["python", "app.pyz"]
        })
    if language == "go":
        project_serv.update({
            "command": [f"./{project_name}"]
        })

    # nfs
    if nfs_addr:
        if use_nfs_v4:
            compose.update({
                "volumes": {
                    "mynfs": {
                        "driver": "local",
                        "driver_opts": {
                            "type": "nfs",
                            "o": f"addr={nfs_addr},rw,nfsvers=4,async",
                            "device": nfs_shared_path}
                    }
                }
            })
        else:
            compose.update({
                "volumes": {
                    "mynfs": {
                        "driver": "local",
                        "driver_opts": {
                            "type": "nfs",
                            "o": f"addr={nfs_addr},nolock,soft,rw",
                            "device": nfs_shared_path
                        }
                    }
                }
            })
        project_serv.update({
            "volumes": ["mynfs:/shared_data"]
        })

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

        # deploy
        project_serv.update({
            "cpus": "0.5",
            "mem_limit": "256m",
            "mem_reservation": "64m",
            "restart": "on-failure",
        })

    elif compose_version == "3.7":
        # 3.7 special
        # networks
        if use_host_network:
            compose.update(
                {
                    "networks": {
                        "myhostnetwork": {
                            "external": True,
                            "name": "host"
                        }
                    }
                }
            )
            project_serv.update({
                "networks": ["myhostnetwork"]
            })
        else:
            if ports:
                project_serv.update({
                    "ports": ports
                })
        # deploy
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
        # 3.8 special
        if use_host_network:
            compose.update(
                {
                    "networks": {
                        "myhostnetwork": {
                            "external": True,
                            "name": "host"
                        }
                    }
                }
            )
            project_serv.update({
                "networks": ["myhostnetwork"]
            })
        else:
            if ports:
                project_serv.update({
                    "ports": ports
                })
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
        warnings.warn("未支持的docker-compose版本")
        return

    project_serv_name = project_name or "app"
    services.update({
        project_serv_name: project_serv
    })

    if add_service:
        for serice_name in add_service:
            if serice_name == "redis":
                services.update(
                    {
                        "redis": {
                            "image": "redis:latest",
                            "mem_limit": "500m",
                            "restart": "on-failure",
                            "ports": ["6379:6379"]
                        }
                    }
                )
            elif serice_name == "postgres":
                services.update(
                    {
                        "postgres": {
                            "image": "timescale/timescaledb-postgis:latest-pg13",
                            "mem_limit": "500m",
                            "restart": "on-failure",
                            "ports": ["5432:5432"],
                            "environment": {
                                "POSTGRES_PASSWORD": postgres
                            },
                            "volumes": [
                                "postgres_data:/var/lib/postgresql/data"
                            ],
                            "command": ["-c", "max_connections=300"]
                        }
                    }
                )
            elif serice_name == "zookeeper":
                for i in range(1, 4):
                    zookeeper_sers = {
                        "image": "zookeeper",
                        "hostname": f"zoo{i}",
                        "ports": ["2181:2181"],
                        "mem_limit": "500m",
                        "restart": "on-failure",
                        "environment": {
                            "ZOO_MY_ID": i,
                            "ZOO_SERVERS": "server.1=0.0.0.0:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181"
                        }
                    }
                    services.update(
                        {
                            f"zoo{i}": zookeeper_sers
                        }
                    )
            elif serice_name == "envoy":
                services.update(
                    {
                        "envoy": {
                            "image": "envoyproxy/envoy-dev:76286f6152666c73d9379f21f43152bd03b00f78",
                            "hostname": f"zoo{i}",
                            "ports": ["10000:10000"],
                            "mem_limit": "500m",
                            "restart": "on-failure",
                            "volumes": ["./envoy.yaml:/etc/envoy/envoy.yaml"]
                        }
                    }
                )

    compose.update(
        {
            "services": services
        }
    )
    content = pyaml.dump(compose, sort_dicts=False, force_embed=False)
    with open(cwdp.joinpath(dockercompose_name), "w", newline="", encoding="utf-8") as f:
        f.write(content.replace("default_log: *default_log", "").replace("default_extra_hosts: *default_extra_hosts", ""))
