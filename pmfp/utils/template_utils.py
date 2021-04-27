"""模板相关的通用工具."""
import json
from pathlib import Path
from configparser import ConfigParser
# from string import Template
from jinja2 import Template
from typing import Any


def template_2_content(template: str, **kwargs: Any) -> str:
    """将模板转换为文件内容.

    Args:
        template (str): 模板字符串
        kwargs (Dict[str,str]): 由模板构造内容的关键字

    """
    try:
        template_content = Template(template)
        # content = template_content.safe_substitute(
        #     **kwargs
        # )
        content = template_content.render(
            **kwargs
        )
    except Exception:
        print("template_2_content出错")
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

    except Exception:
        print("template_2_content出错")
        raise
    else:
        return json.dumps(content, indent=4, ensure_ascii=False, sort_keys=True)


def cfgtemplate_2_file(template: str, file: Path, **kwargs: Any) -> None:
    """将模板转换为文件内容.

    Args:
        template (str): 模板字符串
        file (Path): 文件保存位置
        kwargs (Dict[str,str]): 由模板构造内容的关键字

    """
    try:
        config = ConfigParser()
        config.read_string(template)
        for section, kvs in kwargs.items():
            for k, v in kvs.items():
                config[section][k] = v
    except Exception:
        print("template_2_content出错")
        raise
    else:
        if not file.exists():
            file.touch()
        with open(file, "w", newline="", encoding="utf-8") as f:
            config.write(f)
