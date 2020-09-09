from pathlib import Path
import shutil
from .fs_utils import tempdir
from .git_utils import git_clone,get_latest_commit

class SourcePack:
    """资源包类."""

    TENPLATE_URL = "{host}::{repo_name}::{tag}"
    @classmethod
    def from_sourcepack_string(cls, sourcepack_string: str) -> "SourcePack":
        """从资源包字符串构造资源包对象."""
        host, repo_name, tag = sourcepack_string.split("::")
        return cls(host=host, repo_name=repo_name, tag=tag)

    def __init__(self, repo_name: str, *,
                 tag: str = "latest", host: str = "github.com") -> None:
        """构造资源包对象.

        Args:
            tag (str): 标签或者"latest"
            repo_name (str): 仓库名
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

    def git_url(self,schema="https")->str:
        """构造资源包的git仓库地址."""
        return f"{schema}://{self.host}/{self.repo_name}.git"

    def _clone_source_pack(self,temp_dir:Path):
        url = self.git_url()
        to = temp_dir.as_posix()
        def clone_succ_cb(content:str)->None:
            if self.tag == "latest":
                self.tag = get_latest_commit(to)
            tempalte_dir = self.source_pack_path(temp_dir.parent)
            for p in temp_dir.iterdir():
                if ".git" not in p.name:
                    try:
                        shutil.move(str(p),str(tempalte_dir.joinpath(p.name)))
                    except Exception as e:
                        print(f"移动{p.name}出错: {e}")
                    

        if self.tag == "latest":
            branch = "master"
        else:
            branch = self.tag
        git_clone(url, to,branch=branch,
              succ_cb= clone_succ_cb,
            )
        print("_clone_source_pack 执行完成")

    def clone_source_pack(self,cache_dir:str)->None:
        """克隆资源包到本地缓存临时文件夹."""
        tempdir(cache_dir,cb=self._clone_source_pack)

    def source_pack_path(self,cache_dir_path:Path)->Path:
        """构造资源包的本地路径."""
        return cache_dir_path.joinpath(f"{self.host}/{self.repo_name}/{self.tag}")


    def cache(self, cache_dir: str) -> None:
        """缓存资源包到本地."""
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
        """从组件模板字符串构造组件模板对象."""
        host, repo_name, tag, component_path = component_string.split("::")
        source_pack= SourcePack(repo_name=repo_name, tag=tag, host=host)
        return cls(component_path=component_path,source_pack=source_pack)

    def __init__(self, component_path: str, source_pack:SourcePack) -> None:
        """构造组件模板对象.

        Args:
            tag (str): 标签或者"latest"
            repo_name (str): 仓库名
            component_path (str): 组件的相对地址
            host (str, optional): git仓库的host. Defaults to "https://github.com".

        """
        self.source_pack = source_pack
        self.component_path = component_path

    def as_component_string(self) -> str:
        """构造组件模板字符串."""
        return self.TENPLATE_URL.format(
            host=self.source_pack.host,
            repo_name=self.source_pack.repo_name,
            tag=self.source_pack.tag,
            component_path=self.component_path
        )

    def to_component(self,cache_dir:str, root: str, **kwargs: str):
        pass