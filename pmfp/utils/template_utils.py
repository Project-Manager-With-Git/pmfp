"""模板相关的通用工具."""
import json
from string import Template
from typing import Any
from pmfp.const import PMFP_CONFIG_PATH,PMFP_CONFIG_HOME,DEFAULT_PMFPRC


def template_2_content(template: str, **kwargs: Any) -> str:
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


def jsontemplate_2_content(template: str, **kwargs: Any) -> str:
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
        return json.dumps(content, indent=4, ensure_ascii=False, sort_keys=True)


