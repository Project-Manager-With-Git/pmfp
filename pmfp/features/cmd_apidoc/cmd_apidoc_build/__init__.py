from typing import Dict, Any, List,Optional
from .build_py import apidoc_build_py


def build_apidoc(language:str,code:str,output:str,source_dir:str,*,project_name:str,author:str, version:str)->None:
    """对指定代码做单元测试.

    Args:
        language (str): 目标语言
        testcode (str): 目标测试代码
        coverage (Optional[bool]): 是否输出检测的覆盖率文档
        source (Optional[List[str]]): 测试覆盖代码
        output (Optional[str]): 覆盖率文档位置

    """
    if language == "py":
        apidoc_build_py(code=code,output=output,source_dir=source_dir,project_name=project_name,author=author, version=version)
    
    else:
        print(f"未支持的语言{language}")