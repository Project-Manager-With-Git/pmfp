"""编译protobuf的schema为不同语言的代码."""
from typing import Dict, Any, List,Optional
from .new_py import apidoc_new_py

def new_apidoc(language:str,code:str,output:str,source_dir:str,*,root:str,project_name:str,author:str, version:str)->None:
    """对指定代码做单元测试.

    Args:
        language (str): 目标语言
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置

    """
    if language == "py":
        apidoc_new_py(code=code,output=output,source_dir=source_dir,root=root,project_name=project_name,author=author, version=version)
    
    else:
        print(f"未支持的语言{language}")
