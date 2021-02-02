"""远程资源缓存相关的通用工具."""
from pathlib import Path
import shutil
from .fs_utils import tempdir
from .git_utils import git_clone, get_master_latest_commit


class SourcePack:
    """资源包类."""

    TENPLATE_URL = "{host}::{repo_name}::{tag}"

    @classmethod
    def from_sourcepack_string(cls, sourcepack_string: str) -> "SourcePack":
        """从资源包字符串构造资源包对象.

        Args:
            sourcepack_string (str): 用于描述资源包的字符串,其形式为`"{host}::{repo_name}::{tag}"`

        Returns:
            [SourcePack]: 资源包对象.

        """
        host, repo_name, tag = sourcepack_string.split("::")
        return cls(host=host, repo_name=repo_name, tag=tag)

    def __init__(self, repo_name: str, *,
                 tag: str = "latest",
                 host: str = "github.com") -> None:
        """构造资源包对象.

        Args:
            repo_name (str): 仓库名
            tag (str): 标签或者"latest". Defaults to "latest".
            host (str, optional): git仓库的host. Defaults to "github.com".

        """
        self.host = host
        self.repo_name = repo_name
        self.tag = tag

    def as_sourcepack_string(self) -> str:
        """构造资源包字符串."""
        return self.TENPLATE_URL.format(
            host=self.host,
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
        return f"{schema}://{self.host}/{self.repo_name}.git"

    def _clone_source_pack(self, temp_dir: Path) -> None:
        url = self.git_url()
        if self.tag == "latest":
            branch = "master"
        else:
            branch = self.tag
        git_clone(url, temp_dir, branch=branch)
        if self.tag == "latest":
            self.tag = get_master_latest_commit(temp_dir)
        tempalte_dir = self.source_pack_path(temp_dir.parent)
        if not temp_dir.joinpath("ispmfpsource").exists():
            print("git项目不是pmfp的资源项目,清理下载的缓存")
            shutil.rmtree(temp_dir)
            print("清理下载的缓存完成")
            return None
        for p in temp_dir.iterdir():
            if ".git" not in p.name:
                try:
                    shutil.move(str(p), str(tempalte_dir.joinpath(p.name)))
                except Exception as e:
                    print(f"移动{p.name}出错: {e}")
        print("_clone_source_pack 执行完成")

    def clone_source_pack(self, cache_dir: Path) -> None:
        """克隆资源包到本地缓存临时文件夹.

        Args:
            cache_dir (Path): 缓存文件夹地址.

        """
        tempdir(cache_dir, cb=self._clone_source_pack)

    def source_pack_path(self, cache_dir: Path) -> Path:
        """构造资源包的本地路径.

        Args:
            cache_dir (Path): 缓存文件夹路径.

        Returns:
            Path: 资源包所在的文件夹路径

        """
        return cache_dir.joinpath(f"{self.host}/{self.repo_name}/{self.tag}")

    def cache(self, cache_dir: Path) -> None:
        """缓存资源包到本地.

        Args:
            cache_dir (Path): 缓存文件夹地址.

        """
        if self.tag != "latest" and self.source_pack_path(Path(cache_dir)).exists():
            print(f"资源缓存{self.as_sourcepack_string()}已经存在")
        else:
            self.clone_source_pack(cache_dir)
            print(f"资源缓存{self.as_sourcepack_string()}缓存成功")


class ComponentTemplate:
    """组件模板类."""

    TENPLATE_URL = "{host}::{repo_name}::{tag}::{component_path}"

    @classmethod
    def from_component_string(cls, component_string: str) -> "ComponentTemplate":
        """从组件模板字符串构造组件模板对象.

        组件模板字符串的形式为`"{host}::{repo_name}::{tag}::{component_path_str}"`

        Returns:
            [ComponentTemplate]: 组件模板对象

        """
        host, repo_name, tag, component_path_str = component_string.split("::")
        source_pack = SourcePack(repo_name=repo_name, tag=tag, host=host)
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
            repo_name=self.source_pack.repo_name,
            tag=self.source_pack.tag,
            component_path=self.component_path
        )

    def to_component(self, cache_dir: str, root: str, **kwargs: str) -> None:
        pass
