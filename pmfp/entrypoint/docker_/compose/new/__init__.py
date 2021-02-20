import warnings
from typing import Optional
import pyaml
from .core import dockercompose_new


@dockercompose_new
def new_dockercompose(project_name: str, docker_register_namespace: str, version: str, compose_version: str,
                      dockercompose_name: str = "docker-compose.yml", docker_register: Optional[str] = None,
                      nfs_addr: Optional[str] = None, nfs_shared_path: str = "/", use_nfs_v4: bool = False,
                      language: Optional[str] = None, extend: bool = False, fluentd_url: Optional[str] = None,
                      extra_hosts: Optional[List[str]] = None, use_host_network: bool = False, cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
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
        "version": compose_version,
        "x-log": default_log,
        "default_log": default_log,
    }

    docker_register = docker_register if docker_register else ""
    project_serv = {
        "image": f"{docker_register}/{docker_register_namespace}/{project_name}:{version}",
        "logging": {
            "<<": default_log
        },
    }
    if extra_hosts:
        default_extra_hosts = {
            "extra_hosts": extra_hosts
        }
        compose.update({
            "x-extra_hosts": default_extra_hosts,
            "default_extra_hosts": default_extra_hosts,
        })
        project_serv.update{
            "<<": default_extra_hosts
        }
    if language == "py" and extend is True:
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

    if nfs_addr:
        if use_nfs_v4:
            compose.update({
                "volumes": {
                    "mynfs": {
                        "driver": "local"
                        "driver_opts": {
                            "type": "nfs"
                            "o": f"addr={nfs_addr},rw,nfsvers=4,async"
                            "device": nfs_shared_path
                        }
                    }
                }
            })
        else:
            compose.update({
                "volumes": {
                    "mynfs": {
                        "driver": "local"
                        "driver_opts": {
                            "type": "nfs"
                            "o": f"addr={nfs_addr},nolock,soft,rw"
                            "device": nfs_shared_path
                        }
                    }
                }
            })
        project_serv.update({
            "volumes": ["mynfs:/shared_data"]
        })

    if compose_version == "2.4":
        if use_host_network:
            project_serv.update({
                "network_mode": "host"
            })
        project_serv.update(
            "cpus": 0.5
            "mem_limit": "256m"
            "mem_reservation": "64m",
            "restart": "on-failure"
            "environment": {
                project_name.upper() + "_LOG_LEVEL": "DEBUG"
            }
        )
        services = {
            project_name: project_serv
        }
        compose.update(
            {
                "services": services
            }
        )
    elif compose_version == "3.7":
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
        project_serv.update(
            "environment": {
                project_name.upper() + "_LOG_LEVEL": "DEBUG"
            },
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
                }
                "placement": {
                    "constraints": ["node.role==manager", "engine.labels.operatingsystem==ubuntu 18.04"],
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
        )
        services = {
            project_name: project_serv
        }
        compose.update(
            {
                "services": services
            }
        )
    elif compose_version == "3.8":
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
        project_serv.update(
            "environment": {
                project_name.upper() + "_LOG_LEVEL": "DEBUG"
            },
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
                }
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
        )
        services = {
            project_name: project_serv
        }
        compose.update(
            {
                "services": services
            }
        )
    else:
        warnings.warn("未支持的docker-compose版本")
        return
    content = pyaml.dump(compose, sort_dicts=False, force_embed=False)
    with open(cwdp.joinpath(dockercompose_name), "w", newline="", encoding="utf-8") as f:
        f.write(content.replace("default_log: *default_log", "").replace("default_extra_hosts: *default_extra_hosts", ""))
