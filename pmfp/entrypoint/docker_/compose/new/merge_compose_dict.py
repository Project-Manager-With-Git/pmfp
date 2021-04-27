from typing import Optional
from .typedef import (
    NetworksSchema,
    ServiceSchema,
    ServicesSchema,
    ComposeSchema
)


def level1(old: ComposeSchema, new: ComposeSchema) -> ComposeSchema:
    """尽量更新."""
    old_log = new.get("x-log")
    old_services: Optional[ServicesSchema] = old.get("services")
    old_networks = old.get("networks")
    old_volumes = old.get("volumes")
    old_configs = old.get("configs")
    old_secrets = old.get("secrets")

    new_version = new["version"]
    new_log = new.get("x-log")
    new_services = new.get("services")
    new_networks = new.get("networks")
    new_volumes = new.get("volumes")
    new_configs = new.get("configs")
    new_secrets = new.get("secrets")

    result: ComposeSchema = {}
    result["version"] = new_version

    # log
    if new_log:
        result["x-log"] = new_log
    else:
        if old_log:
            result["x-log"] = old_log
    # services
    services = {}
    if old_services:
        services.update(old_services)
    if new_services:
        services.update(new_services)
    if services:
        result["services"] = services
    # networks
    networks = {}
    if old_networks:
        networks.update(old_networks)
    if new_networks:
        networks.update(new_networks)
    if networks:
        result["networks"] = networks

    # volumes
    volumes = {}
    if old_volumes:
        volumes.update(old_volumes)
    if new_volumes:
        volumes.update(new_volumes)
    if volumes:
        result["volumes"] = volumes

    # configs
    configs = {}
    if old_configs:
        configs.update(old_configs)
    if new_configs:
        configs.update(new_configs)
    if configs:
        result["configs"] = configs

    # secrets
    secrets = {}
    if old_secrets:
        secrets.update(old_secrets)
    if new_secrets:
        secrets.update(new_secrets)
    if secrets:
        result["secrets"] = secrets

    return result


def level2(old: ComposeSchema, new: ComposeSchema, project_name: str = "app") -> ComposeSchema:
    old_version = old["version"]
    old_log = new.get("x-log")
    old_services: Optional[ServicesSchema] = old.get("services")
    old_other_servs: ServicesSchema = {}
    old_project_serv: ServiceSchema = {}
    if old_services:
        for service_name, service_conf in old_services.items():
            if service_name == project_name:
                old_project_serv = service_conf
            else:
                old_other_servs[service_name] = service_conf
    old_networks = old.get("networks")
    old_volumes = old.get("volumes")
    old_configs = old.get("configs")
    old_secrets = old.get("secrets")

    new_version = new["version"]
    new_log = new.get("x-log")
    new_services = new.get("services")
    new_other_servs: ServicesSchema = {}
    new_project_serv: ServiceSchema = {}
    if new_services:
        for service_name, service_conf in new_services.items():
            if service_name == project_name:
                new_project_serv = service_conf
            else:
                new_other_servs[service_name] = service_conf

    new_networks = new.get("networks")
    new_volumes = new.get("volumes")
    new_configs = new.get("configs")
    new_secrets = new.get("secrets")

    result: ComposeSchema = {}
    result["version"] = new_version

    # log
    if new_log:
        result["x-log"] = new_log
    else:
        if old_log:
            result["x-log"] = old_log

    # services
    services = {}
    if old_other_servs:
        services.update(old_other_servs)
    if new_other_servs:
        services.update(new_other_servs)
    project_serv: ServiceSchema = {}
    if old_project_serv:
        project_serv.update(old_project_serv)
    if new_project_serv:
        project_serv.update(new_project_serv)
    services[project_name] = project_serv
    if services:
        result["services"] = services
    # networks
    networks = {}
    if old_networks:
        networks.update(old_networks)
    if new_networks:
        networks.update(new_networks)
    if networks:
        result["networks"] = networks

    # volumes
    volumes = {}
    if old_volumes:
        volumes.update(old_volumes)
    if new_volumes:
        volumes.update(new_volumes)
    if volumes:
        result["volumes"] = volumes

    # configs
    configs = {}
    if old_configs:
        configs.update(old_configs)
    if new_configs:
        configs.update(new_configs)
    if configs:
        result["configs"] = configs

    # secrets
    secrets = {}
    if old_secrets:
        secrets.update(old_secrets)
    if new_secrets:
        secrets.update(new_secrets)
    if secrets:
        result["secrets"] = secrets
    return result


def level3(old: ComposeSchema, new: ComposeSchema, project_name: str = "app") -> ComposeSchema:
    old_version = old["version"]
    old_log = new.get("x-log")
    old_services: Optional[ServicesSchema] = old.get("services")
    old_other_servs: ServicesSchema = {}
    old_project_serv: ServiceSchema = {}
    if old_services:
        for service_name, service_conf in old_services.items():
            if service_name == project_name:
                old_project_serv = service_conf
            else:
                old_other_servs[service_name] = service_conf
    old_networks = old.get("networks")
    old_volumes = old.get("volumes")
    old_configs = old.get("configs")
    old_secrets = old.get("secrets")

    new_version = new["version"]
    new_log = new.get("x-log")
    new_services = new.get("services")
    new_other_servs: ServicesSchema = {}
    new_project_serv: ServiceSchema = {}
    if new_services:
        for service_name, service_conf in new_services.items():
            if service_name == project_name:
                new_project_serv = service_conf
            else:
                new_other_servs[service_name] = service_conf

    new_networks = new.get("networks")
    new_volumes = new.get("volumes")
    new_configs = new.get("configs")
    new_secrets = new.get("secrets")

    result: ComposeSchema = {}
    result["version"] = new_version

    # log
    if old_log:
        result["x-log"] = old_log
    else:
        if new_log:
            result["x-log"] = new_log

    # services
    services = {}
    if old_other_servs:
        services.update(old_other_servs)
    if new_other_servs:
        for sn, sc in new_other_servs.items():
            if sn not in old_other_servs:
                services[sn] = sc
    project_serv: ServiceSchema = {}
    if old_project_serv:
        project_serv.update(old_project_serv)
    if new_project_serv:
        project_serv.update(new_project_serv)
    services[project_name] = project_serv
    if services:
        result["services"] = services
    # networks
    networks: NetworksSchema = {}
    if old_networks:
        networks.update(old_networks)
    else:
        old_networks = {}
    if new_networks:
        for nn, nc in new_networks.items():
            if nn not in old_networks.keys():
                networks[nn] = nc
    if networks:
        result["networks"] = networks

    # volumes
    volumes = {}
    if old_volumes:
        volumes.update(old_volumes)
    else:
        old_volumes = {}
    if new_volumes:
        for vn, vc in new_volumes.items():
            if vn not in old_volumes.keys():
                volumes[vn] = vc
    if volumes:
        result["volumes"] = volumes

    # configs
    configs = {}
    if old_configs:
        configs.update(old_configs)
    else:
        old_configs = {}
    if new_configs:
        for cn, cc in new_configs.items():
            if cn not in old_configs.keys():
                configs[cn] = cc
    if configs:
        result["configs"] = configs

    # secrets
    secrets = {}
    if old_secrets:
        secrets.update(old_secrets)
    else:
        old_secrets = {}
    if new_secrets:
        for cn, cc in new_secrets.items():
            if cn not in old_secrets.keys():
                secrets[cn] = cc
    if secrets:
        result["secrets"] = secrets
    return result


def level4(old: ComposeSchema, new: ComposeSchema, project_name: str = "app") -> ComposeSchema:
    old_version = old["version"]
    old_log = new.get("x-log")
    old_services: Optional[ServicesSchema] = old.get("services")
    old_other_servs: ServicesSchema = {}
    old_project_serv: ServiceSchema = {}
    if old_services:
        for service_name, service_conf in old_services.items():
            if service_name == project_name:
                old_project_serv = service_conf
            else:
                old_other_servs[service_name] = service_conf
    old_networks = old.get("networks")
    old_volumes = old.get("volumes")
    old_configs = old.get("configs")
    old_secrets = old.get("secrets")

    new_version = new["version"]
    new_log = new.get("x-log")
    new_services = new.get("services")
    new_other_servs: ServicesSchema = {}
    new_project_serv: ServiceSchema = {}
    if new_services:
        for service_name, service_conf in new_services.items():
            if service_name == project_name:
                new_project_serv = service_conf
            else:
                new_other_servs[service_name] = service_conf

    new_networks = new.get("networks")
    new_volumes = new.get("volumes")
    new_configs = new.get("configs")
    new_secrets = new.get("secrets")

    result: ComposeSchema = {}
    result["version"] = new_version

    # log
    if new_log:
        result["x-log"] = new_log
    else:
        if old_log:
            result["x-log"] = old_log
    # services
    services = {}
    if old_other_servs:
        services.update(old_other_servs)
    if new_other_servs:
        services.update(new_other_servs)
    project_serv: ServiceSchema = {}
    if old_project_serv:
        project_serv.update(old_project_serv)
    if new_project_serv:
        for key, value in project_serv.items():
            if isinstance(value, list):
                if new_project_serv.get(key):
                    if isinstance(new_project_serv.get(key), list):
                        project_serv[key] = list(set(new_project_serv.get(key)) | set(value))
                    else:
                        project_serv[key] = new_project_serv.get(key)
            elif isinstance(value, dict):
                if new_project_serv.get(key):
                    if isinstance(new_project_serv.get(key), dict):
                        project_serv[key].update(new_project_serv.get(key))
                    else:
                        project_serv[key] = new_project_serv.get(key)
            else:
                if new_project_serv.get(key):
                    project_serv[key] = new_project_serv.get(key)

        for k, v in new_project_serv.items():
            if k not in project_serv:
                project_serv[k] = v
    services[project_name] = project_serv

    if services:
        result["services"] = services

    # networks
    networks = {}
    if old_networks:
        networks.update(old_networks)
    if new_networks:
        networks.update(new_networks)
    if networks:
        result["networks"] = networks

    # volumes
    volumes = {}
    if old_volumes:
        volumes.update(old_volumes)
    if new_volumes:
        volumes.update(new_volumes)
    if volumes:
        result["volumes"] = volumes

    # configs
    configs = {}
    if old_configs:
        configs.update(old_configs)
    if new_configs:
        configs.update(new_configs)
    if configs:
        result["configs"] = configs

    # secrets
    secrets = {}
    if old_secrets:
        secrets.update(old_secrets)
    if new_secrets:
        secrets.update(new_secrets)
    if secrets:
        result["secrets"] = secrets
    return result


def level5(old: ComposeSchema, new: ComposeSchema, project_name: str = "app") -> ComposeSchema:
    old_log = new.get("x-log")
    old_services: Optional[ServicesSchema] = old.get("services")
    old_other_servs: ServicesSchema = {}
    old_project_serv: ServiceSchema = {}
    if old_services:
        for service_name, service_conf in old_services.items():
            if service_name == project_name:
                old_project_serv = service_conf
            else:
                old_other_servs[service_name] = service_conf
    old_networks = old.get("networks")
    old_volumes = old.get("volumes")
    old_configs = old.get("configs")
    old_secrets = old.get("secrets")

    new_version = new["version"]
    new_log = new.get("x-log")
    new_services = new.get("services")
    new_other_servs: ServicesSchema = {}
    new_project_serv: ServiceSchema = {}
    if new_services:
        for service_name, service_conf in new_services.items():
            if service_name == project_name:
                new_project_serv = service_conf
            else:
                new_other_servs[service_name] = service_conf

    new_networks = new.get("networks")
    new_volumes = new.get("volumes")
    new_configs = new.get("configs")
    new_secrets = new.get("secrets")

    result: ComposeSchema = {}
    result["version"] = new_version

    # log
    if old_log:
        result["x-log"] = old_log
    else:
        if new_log:
            result["x-log"] = new_log

    # services
    services = {}
    if old_other_servs:
        services.update(old_other_servs)
    if new_other_servs:
        for sn, sc in new_other_servs.items():
            if sn not in old_other_servs:
                services[sn] = sc
    project_serv: ServiceSchema = {}
    if old_project_serv:
        project_serv.update(old_project_serv)
    if new_project_serv:
        for key, value in project_serv.items():
            if key in ("deploy", "cpus", "mem_limit", "mem_reservation", "restart",):
                continue
            new_project_compose = new_project_serv.get(key)
            if new_project_compose:
                if isinstance(value, list):
                    if isinstance(new_project_compose, list):
                        project_serv[key] = list(set(new_project_compose) | set(value))
                    else:
                        project_serv[key] = new_project_compose
                elif isinstance(value, dict):
                    if isinstance(new_project_compose, dict):
                        project_serv[key].update(new_project_serv.get(key))
                    else:
                        project_serv[key] = new_project_compose
                else:

                    project_serv[key] = new_project_compose

        for k, v in new_project_serv.items():
            if k not in project_serv:
                project_serv[k] = v
    services[project_name] = project_serv
    if services:
        result["services"] = services
    # networks
    networks: NetworksSchema = {}
    if old_networks:
        networks.update(old_networks)
    else:
        old_networks = {}
    if new_networks:
        for nn, nc in new_networks.items():
            if nn not in old_networks.keys():
                networks[nn] = nc
    if networks:
        result["networks"] = networks

    # volumes
    volumes = {}
    if old_volumes:
        volumes.update(old_volumes)
    else:
        old_volumes = {}
    if new_volumes:
        for vn, vc in new_volumes.items():
            if vn not in old_volumes.keys():
                volumes[vn] = vc
    if volumes:
        result["volumes"] = volumes

    # configs
    configs = {}
    if old_configs:
        configs.update(old_configs)
    else:
        old_configs = {}
    if new_configs:
        for cn, cc in new_configs.items():
            if cn not in old_configs.keys():
                configs[cn] = cc
    if configs:
        result["configs"] = configs

    # secrets
    secrets = {}
    if old_secrets:
        secrets.update(old_secrets)
    else:
        old_secrets = {}
    if new_secrets:
        for cn, cc in new_secrets.items():
            if cn not in old_secrets.keys():
                secrets[cn] = cc
    if secrets:
        result["secrets"] = secrets
    return result


def merge_compose(old: ComposeSchema, new: ComposeSchema, project_name: str = "app", updatemode: str = "level5") -> ComposeSchema:
    if updatemode == "cover":
        return new
    elif updatemode == "level1":
        return level1(old, new)
    elif updatemode == "level2":
        return level2(old, new, project_name)
    elif updatemode == "level3":
        return level3(old, new, project_name)
    elif updatemode == "level4":
        return level4(old, new, project_name)
    elif updatemode == "level5":
        return level5(old, new, project_name)
    else:
        raise AttributeError(f"un support updatemode {updatemode}")
