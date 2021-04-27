from typing import Dict, List, Union, Optional, Sequence
from mypy_extensions import TypedDict


LogSchema = TypedDict("LogSchema", {
    "driver": str,
    "options": Dict[str, str]
}, total=False)


DriverOptsSchema = TypedDict("DriverOptsSchema", {
    "type": str,
    "o": str,
    "device": str
}, total=False)


ExternalSchema = TypedDict("ExternalSchema", {
    "name": str
})


VolumeSchema = TypedDict("VolumeSchema", {
    "external": Union[bool, ExternalSchema],
    "driver": str,
    "driver_opts": DriverOptsSchema,
    "labels": List[str],
    "name": str
}, total=False)


VolumesSchema = Dict[str, Optional[VolumeSchema]]

IpamConfigSchema = TypedDict("IpamConfigSchema", {
    "subnet": str
})


IpamSchema = TypedDict("IpamSchema", {
    "driver": str,
    "config": IpamConfigSchema
}, total=False)


NetworkSchema = TypedDict("NetworkSchema", {
    "driver": str,
    "driver_opts": Dict[str, str],
    "attachable": bool,
    "enable_ipv6": bool,
    "ipam": IpamSchema,
    "internal": bool,
    "labels": List[str],
    "external": Union[bool, ExternalSchema],
    "name": str
}, total=False)


NetworksSchema = Dict[str, Optional[NetworkSchema]]


ConfigAndSecretSchema = TypedDict("ConfigAndSecretSchema", {
    "file": str,
    "external": Union[bool, ExternalSchema],
    "name": str
}, total=False)


BuildSchema = TypedDict("BuildSchema", {"context": str, "dockerfile": str}, total=False)


PortSchema = TypedDict("PortSchema", {
    "target": int,
    "published": int,
    "protocol": str,
    "mode": str
}, total=False)

ResourceSchema = TypedDict("ResourceSchema", {
    "cpus": str,
    "memory": str
}, total=False)

ResourcesSchema = TypedDict("ResourcesSchema", {
    "limits": ResourceSchema,
    "reservations": ResourceSchema
}, total=False)


RestartPolicySchema = TypedDict("RestartPolicySchema", {
    "condition": str,
    "delay": str,
    "max_attempts": int,
    "window": str
}, total=False)


PlacementSchema = TypedDict("PlacementSchema", {
    "constraints": List[str],
    "preferences": List[str],
    "max_replicas_per_node": int
}, total=False)


UpdateAndRollbackConfigSchema = TypedDict("UpdateAndRollbackConfigSchema", {
    "parallelism": int,
    "delay": str,
    "failure_action": str,
    "monitor": str,
    "max_failure_ratio": int,
    "order": str
}, total=False)


DeploySchema = TypedDict("DeploySchema", {
    "mode": str,
    "replicas": int,
    "resources": ResourcesSchema,
    "restart_policy": RestartPolicySchema,
    "placement": PlacementSchema,
    "update_config": UpdateAndRollbackConfigSchema,
    "rollback_config": UpdateAndRollbackConfigSchema
}, total=False)

LoggingAliasSchema = TypedDict("LoggingAliasSchema", {
    "<<": LogSchema
})


ServiceSchema = TypedDict("ServiceSchema", {
    "hostname": str,
    "image": str,
    "build": Union[str, BuildSchema],
    "logging": Union[LogSchema, LoggingAliasSchema],
    "network_mode": str,
    "extra_hosts": List[str],
    "networks": List[str],
    "ports": Sequence[Union[str, PortSchema]],
    "volumes": List[str],
    "configs": List[str],
    "secrets": List[str],
    "environment": Union[Dict[str, str], List[str]],
    "command": Union[str, List[str]],
    "cpus": str,
    "mem_limit": str,
    "mem_reservation": str,
    "restart": str,
    "scale": int,
    "deploy": DeploySchema
}, total=False)


ServicesSchema = Dict[str, ServiceSchema]


ComposeSchema = TypedDict("ComposeSchema", {
    "version": str,
    "x-log": LogSchema,
    "services": ServicesSchema,
    "networks": NetworksSchema,
    "volumes": VolumesSchema,
    "configs": Dict[str, ConfigAndSecretSchema],
    "secrets": Dict[str, ConfigAndSecretSchema],
}, total=False)
