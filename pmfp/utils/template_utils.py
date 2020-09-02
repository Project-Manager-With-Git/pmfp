"""模板相关的通用工具."""
import json
from string import Template
from pathlib import Path
from typing import Dict, Any


def template_2_content(template:str,**kwargs:Any)->str:
    """将模板转换为文件内容.

    Args:
        template (str): 模板字符串
        kwargs (Dict[str,str]): 由模板构造内容的关键字
    
    """
    try:
        template_content = Template(template)
        content = template_content.safe_substitute(
            **kwargs
        )
    except:
        print(f"template_2_content出错")
        raise
    else:
        return content


def jsontemplate_2_content(template:str,**kwargs:Any)->str:
    """将模板转换为文件内容.

    Args:
        template (str): 模板字符串
        kwargs (Dict[str,str]): 由模板构造内容的关键字
    
    """
    try:
        content = json.loads(template)
        content.update(kwargs)

    except:
        print(f"template_2_content出错")
        raise
    else:
        return json.dumps(content, indent=4,ensure_ascii=False,sort_keys=True)



class ComponentTemplate:
    TENPLATE_URL = "{host}::{repo_name}::{tag}::{component_path}"

    @classmethod
    def from_component_string(clz,component_string:str)->"ComponentTemplate":
        host,repo_name,tag,component_path = component_string.split("::")
        return clz(host=host,repo_name=repo_name,tag=tag,component_path=component_path)

    def __init__(self,tag:str,repo_name:str,component_path:str,host:str="https://github.com")->None:
        self.host = host
        self.repo_name = repo_name
        self.tag = tag
        self.component_path = component_path

    def as_component_string(self)->str:
        return TENPLATE_URL.format(
            host=self.host,
            repo_name=self.repo_name,
            tag=self.tag,
            component_path=self.component_path
            )

    def cache(self,cache_root:str)->None:
        pass

    def to_component(self,root:str,**kwargs:str):
        pass



    



    