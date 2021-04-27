"""远程资源缓存相关的通用工具."""
import os
import json
import warnings
from pathlib import Path
import shutil
from typing import Optional
from jsonschema import validate
from pmfp.protocol import TEMPLATE_INFO_SCHEMA
from .fs_utils import remove_readonly
from .git_utils import git_clone, get_master_latest_commit, git_pull_master, make_repod, is_git_dir
from .tools_info_utils import get_config_info


class SourcePack:
    """资源包类."""

    TENPLATE_URL = "{host}::{repo_namespace}::{repo_name}@{tag}"

    @classmethod
    def from_sourcepack_string(cls, sourcepack_string: str) -> "SourcePack":
        """从资源包字符串构造资源包对象.

        Args:
            sourcepack_string (str): 用于描述资源包的字符串,其形式为`"[[{host}::]{repo_namespace}::]{repo_name}[@{tag}]"`

        Returns:
            [SourcePack]: 资源包对象.

        """
        if "@" in sourcepack_string:
            urlinfo, tag = sourcepack_string.split("@")
            try:
                host, repo_namespace, repo_name = urlinfo.split("::")
            except Exception:
                try:
                    repo_namespace, repo_name = urlinfo.split("::")
                except Exception:
                    return cls(repo_name=urlinfo, tag=tag)
                else:
                    return cls(repo_namespace=repo_namespace, repo_name=repo_name, tag=tag)
            else:
                return cls(host=host, repo_namespace=repo_namespace, repo_name=repo_name, tag=tag)
        else:
            try:
                host, repo_namespace, repo_name = sourcepack_string.split("::")
            except Exception:
                try:
                    repo_namespace, repo_name = sourcepack_string.split("::")
                except Exception:
                    return cls(repo_name=sourcepack_string)
                else:
                    return cls(repo_namespace=repo_namespace, repo_name=repo_name)
            else:
                return cls(host=host, repo_namespace=repo_namespace, repo_name=repo_name)

    def __init__(self, repo_name: str, *, repo_namespace: Optional[str] = None,
                 tag: str = "latest",
                 host: Optional[str] = None) -> None:
        """构造资源包对象.

        Args:
            repo_namespace (str): 仓库的命名空间
            repo_name (str): 仓库名
            tag (str): 标签或者"latest". Defaults to "latest".
            host (str, optional): git仓库的host. Defaults to "github.com".

        """
        conf = get_config_info()
        if host:
            self.host = host
        else:
            self.host = conf["default_template_host"]
        if repo_namespace:
            self.repo_namespace = repo_namespace
        else:
            self.repo_namespace = conf["default_template_namespace"]

        self.repo_name = repo_name
        self.tag = tag

    def as_sourcepack_string(self) -> str:
        """构造资源包字符串."""
        return self.TENPLATE_URL.format(
            host=self.host,
            repo_namespace=self.repo_namespace,
            repo_name=self.repo_name,
            tag=self.tag
        )

    def git_url(self, schema: str = "https") -> str:
        """构造资源包的git仓库地址url.

        Args:
            schema (str, optional): url协议. Defaults to "https".

        Returns:
            str: git的仓库地址字符串.

        """
        return f"{schema}://{self.host}/{self.repo_namespace}/{self.repo_name}.git"

    def pull_latest(self, cache_dir: Path, throw: bool = True) -> None:
        """拉取最新镜像,并将原来的版本以hash为tag保存

        Args:
            temp_dir (Path): [description]
            throw (bool): 是否抛出异常
        """
        conf = get_config_info()
        if self.tag != "latest":
            if throw:
                raise AttributeError("only latest tag can pull latest")
            else:
                warnings.warn("only latest tag can pull latest")
                return None
        pack_dir = self.source_pack_path(cache_dir)
        d = make_repod(pack_dir)
        if not is_git_dir(d):
            if throw:
                raise AttributeError(f"目标路径{pack_dir}不是git仓库.")
            else:
                warnings.warn("only latest tag can pull latest")
                return None
        # 保存之前的版本
        commit_hash = get_master_latest_commit(pack_dir)
        copy_dir = pack_dir.parent.joinpath(commit_hash)
        if copy_dir.exists:
            if copy_dir.is_dir():
                shutil.rmtree(copy_dir, onerror=remove_readonly)
                # os.rmdir(copy_dir)
            if copy_dir.is_file():
                os.remove(copy_dir)
        copy_dir.mkdir(parents=True)
        for p in pack_dir.iterdir():
            if p.name.startswith(".") and p.name != conf["template_config_name"]:
                continue
            else:
                if p.is_dir():
                    shutil.copytree(str(p), copy_dir.joinpath(p.name))
                else:
                    shutil.copyfile(str(p), copy_dir.joinpath(p.name))
        # 更新
        try:
            git_pull_master(pack_dir)
        except Exception as e:
            if throw:
                raise e
            else:
                warnings.warn(f"pull repo get error {str(e)}")
        else:
            print("pull_latest 执行完成")

    def clone_source_pack(self, cache_dir: Path, throw: bool = False) -> None:
        """克隆资源包到本地缓存临时文件夹.

        如果资源包的tag不是latest则clone下来后删除.git文件夹,否则保存

        Args:
            cache_dir (Path): 缓存文件夹地址.
            throw (bool): 是否抛出异常
        """
        conf = get_config_info()
        url = self.git_url()
        if self.tag == "latest":
            branch = "master"
        else:
            branch = self.tag
        pack_dir = self.source_pack_path(cache_dir)
        try:
            git_clone(url, pack_dir, branch=branch)
        except Exception as e:
            warnings.warn(f"clone repo get error {str(e)} url: {url} @ {pack_dir}")
            if pack_dir.exists():
                shutil.rmtree(pack_dir, onerror=remove_readonly)
                print("清理下载的缓存完成")
            if throw:
                raise e
            else:
                return None
        else:
            if not pack_dir.joinpath(conf["template_config_name"]).exists():
                warnings.warn("git项目不是pmfp的资源项目,清理下载的缓存")
                shutil.rmtree(pack_dir, onerror=remove_readonly)
                # os.rmdir(pack_dir)
                print("清理下载的缓存完成")
                return None
            else:
                try:
                    with open(pack_dir.joinpath(conf["template_config_name"]), encoding="utf-8") as f:
                        instance = json.load(f)
                    validate(instance=instance, schema=TEMPLATE_INFO_SCHEMA)
                except Exception as e:
                    warnings.warn("项目的pmfp_template.json文件不符合规范")
                    shutil.rmtree(pack_dir, onerror=remove_readonly)
                    # os.rmdir(pack_dir)
                    print("清理下载的缓存完成")
                    if throw:
                        raise e
                    else:
                        return None
                else:
                    if self.tag != "latest":
                        for p in pack_dir.iterdir():
                            if p.name.startswith(".") and p.name != conf["template_config_name"]:
                                if p.is_dir():
                                    shutil.rmtree(p, onerror=remove_readonly)
                                    # os.rmdir(p)
                                if p.is_file():
                                    os.remove(p)
                    print("clone_source_pack 执行完成")

    def source_pack_path(self, cache_dir: Path) -> Path:
        """构造资源包的本地路径.

        Args:
            cache_dir (Path): 缓存文件夹路径.

        Returns:
            Path: 资源包所在的文件夹路径

        """
        return cache_dir.joinpath(f"{self.host}/{self.repo_namespace}/{self.repo_name}/{self.tag}")

    def cache(self, cache_dir: Path, throw_clone: bool = False, throw_pull: bool = False, not_pull: bool = False) -> None:
        """缓存资源包到本地.

        Args:
            cache_dir (Path): 缓存文件夹地址.
            throw (bool): 是否抛出异常

        """
        if self.tag != "latest":
            if self.source_pack_path(cache_dir).exists():
                warnings.warn(f"资源缓存{self.as_sourcepack_string()}已经存在")
            else:
                self.clone_source_pack(cache_dir, throw=throw_clone)

        else:
            if self.source_pack_path(cache_dir).exists():
                if not not_pull:
                    self.pull_latest(cache_dir, throw=throw_pull)
            else:
                self.clone_source_pack(cache_dir, throw=throw_clone)


class ComponentTemplate:
    """组件模板类."""

    TENPLATE_URL = "[{host}::]{repo_namespace}::{repo_name}[@{tag}]//{component_path}"

    @classmethod
    def from_component_string(cls, component_string: str) -> "ComponentTemplate":
        """从组件模板字符串构造组件模板对象.

        组件模板字符串的形式为`"[[{host}::]{repo_namespace}::]{repo_name}[@{tag}]//{component_path_str}"`

        Returns:
            [ComponentTemplate]: 组件模板对象

        """
        sourcepack_string, component_path_str = component_string.split("//")
        source_pack = SourcePack.from_sourcepack_string(sourcepack_string)
        return cls(component_path_str=component_path_str, source_pack=source_pack)

    def __init__(self, component_path_str: str, source_pack: SourcePack) -> None:
        """构造组件模板对象.

        Args:
            component_path_str (str): 组件的相对路径字符串
            source_pack (SourcePack): 组件所在的sourcepack对象.

        """
        self.source_pack = source_pack
        self.component_path = component_path_str

    def as_component_string(self) -> str:
        """构造组件模板字符串."""
        return self.TENPLATE_URL.format(
            host=self.source_pack.host,
            repo_namespace=self.source_pack.repo_namespace,
            repo_name=self.source_pack.repo_name,
            tag=self.source_pack.tag,
            component_path=self.component_path
        )
