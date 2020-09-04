from pathlib import Path
import shutil
from pmfp.utils.fs_utils import tempdir
from pmfp.utils.git_utils import git_clone,get_latest_commit


class ComponentTemplate:
    """组件模板类."""

    TENPLATE_URL = "{host}::{repo_name}::{tag}::{component_path}"

    @classmethod
    def from_component_string(cls, component_string: str) -> "ComponentTemplate":
        """从组件模板字符串构造组件模板对象."""
        host, repo_name, tag, component_path = component_string.split("::")
        return cls(host=host, repo_name=repo_name, tag=tag, component_path=component_path)

    def __init__(self, repo_name: str, component_path: str, *,
                 tag: str = "latest", host: str = "github.com") -> None:
        """构造组件模板对象.

        Args:
            tag (str): 标签或者"latest"
            repo_name (str): 仓库名
            component_path (str): 组件的相对地址
            host (str, optional): git仓库的host. Defaults to "https://github.com".

        """
        self.host = host
        self.repo_name = repo_name
        self.tag = tag
        self.component_path = component_path

    def as_component_string(self) -> str:
        """构造组件模板字符串."""
        return self.TENPLATE_URL.format(
            host=self.host,
            repo_name=self.repo_name,
            tag=self.tag,
            component_path=self.component_path
        )

    def git_url(self,schema="https")->str:
        return f"{schema}://{self.host}/{self.repo_name}.git"

    def _clone_source_pack(self,temp_dir:Path):
        url = self.git_url()
        to = temp_dir.as_posix()
        def clone_succ_cb(content:str)->None:
            if self.tag == "latest":
                self.tag = get_latest_commit(to)
            tempalte_dir = self.source_pack_path(temp_dir.parent)
            for p in temp_dir.iterdir():
                if p.name != ".git":
                    shutil.move(str(p),str(tempalte_dir.joinpath(p.name)))

        if self.tag == "latest":
            branch = "master"
        else:
            branch = self.tag
            git_clone(url, to,branch=branch,
              succ_cb= clone_succ_cb,
            )

    def clone_source_pack(self,cache_dir:str):
        tempdir(cache_dir,cb=self._clone_source_pack)

    def source_pack_path(self,cache_dir_path:Path)->Path:
        return cache_dir_path.joinpath(f"{self.host}/{self.repo_name}/{self.tag}")



    def cache(self, cache_dir: str) -> None:
        if self.tag != "latest" and self.source_pack_path(Path(cache_dir)).exists():
            print(f"资源缓存{self.as_component_string()}已经存在")
        else:
            clone_source_pack(cache_dir)
            print(f"资源缓存{self.as_component_string()}缓存成功")



    def to_component(self,cache_dir:str, root: str, **kwargs: str):
        pass
