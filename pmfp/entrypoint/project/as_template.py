import os
import json
import shutil
import warnings
from pathlib import Path
from typing import Dict, Any
from pmfp.const import GOLBAL_PYTHON_VERSION, DEFAULT_AUTHOR
from pmfp.utils.endpoint import EndPoint
from pmfp.utils.fs_utils import iter_dir_to_end, get_abs_path, tempdir, remove_readonly
from pmfp.utils.tools_info_utils import get_config_info, get_golang_version
from .core import project

acccept_suffix = (".py", ".js", ".ts", ".go", ".c", ".cpp", ".h", ".hpp", ".pyd", ".pyx", ".scala", ".cmake", ".jinja", "md")
except_dir = ("vendor", "node_modules", "dist", "build", "doc", "docs", "document", "documents", "coverage", "__pycache__", "doc_typecheck", "doc_unittest")


class AsTemp(EndPoint):
    """基于项目构造一个模板项目.

    注意只是粗略构造,需要进一步加工.
    """
    _name = "as_temp"
    verify_schema = False
    load_all_config_file = True
    config_file_only_get_need = False
    argparse_noflag = "template_type"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["template_type"],
        "properties": {
            "template_type": {
                "type": "string",
                "description": "模板库的类型,components表示是组件集合,不能用作模板独立构建项目",
                "enum": ["socket", "GUI", "task", "watcher", "module", "components", "doc"]
            },
            "parttens": {
                "type": "array",
                "title": "p",
                "description": "替换源码中的字符串为指定字符串,格式为`<partten_key>::<template_key>::<default_value>`",
                "items": {
                    "type": "string"
                }
            },
            "cwd": {
                "type": "string",
                "description": "项目目录",
                "default": "."
            },
            "to": {
                "type": "string",
                "title": "t",
                "description": "模板放置位置",
                "default": "template"
            },
            "yes": {
                "type": "boolean",
                "title": "y",
                "description": "执行过程中都使用默认填充",
                "default": False
            }
        }
    }

    def do_main(self) -> None:
        cwdp = get_abs_path(self.config["cwd"])
        template_dir = cwdp.joinpath(self.config.get("to", "template"))
        if template_dir.exists():
            print(f"目标路径{template_dir}已经存在,退出")
            return

        yes = self.config.get("yes")
        pmfpconfig = get_config_info()
        if cwdp.joinpath(pmfpconfig["template_config_name"]).exists():
            print("项目模板配置文件已经存在")
            return
        template_info = {}
        if self.config.get("language"):
            template_info["language"] = self.config.get("language")
        else:
            print("项目必须指定语言")
            return
        if self.config.get("env"):
            if yes:
                template_info["env"] = self.config.get("env")
            else:
                yn = input("是否使用项目环境作为模板指定环境? [Y/N]")
                if yn.lower() in ("y", "yes"):
                    template_info["env"] = self.config.get("env")
                yn = ""
        if self.config.get("language") in ("py", "go"):
            if yes:
                if self.config.get("language") == "py":
                    mini_language_version = GOLBAL_PYTHON_VERSION
                elif self.config.get("language") == "go":
                    gv = get_golang_version()
                    if gv:
                        mini_language_version = gv
            else:
                yn = input("是否使用当前环境的语言版本作为模板指定语言最低版本? [Y/N]")
                if yn.lower() in ("y", "yes"):
                    if self.config.get("language") == "py":
                        mini_language_version = GOLBAL_PYTHON_VERSION
                    elif self.config.get("language") == "go":
                        gv = get_golang_version()
                        if gv:
                            mini_language_version = gv
                    template_info["mini_language_version"] = mini_language_version
                yn = ""
        template_info["description"] = ""
        template_info["author"] = self.config.get("author", DEFAULT_AUTHOR)
        template_info["template_type"] = self.config.get("template_type")
        if self.config.get("requires"):
            template_info["requires"] = self.config.get("requires")
        if self.config.get("test_requires"):
            template_info["test_requires"] = self.config.get("test_requires")
        if self.config.get("command"):
            template_info["command"] = self.config.get("command")
        parttens = self.config.get("parttens")
        trans_keys: Dict[str, str] = {}
        if parttens:
            template_keys: Dict[str, Any] = {}
            for pt in parttens:
                partten_key, template_key, default_value = pt.split("::")
                template_keys[template_key] = {
                    "description": "",
                    "default": default_value,
                }
                trans_keys[partten_key] = template_key
            template_info["template_keys"] = template_keys

        components = {}

        def tempcallback(tp: Path) -> None:
            try:
                nonlocal components
                for p in cwdp.iterdir():
                    if p.name.startswith(".") or p.name == tp.name:
                        continue
                    else:
                        if p.is_dir():
                            if p.name not in (pmfpconfig["python_local_env_dir"],
                                              pmfpconfig["default_unittest_doc_dir"],
                                              pmfpconfig["default_typecheck_doc_dir"]) and p.name not in except_dir:
                                components[p.name] = {
                                    "source": p.name,
                                    "description": "",
                                    "default_path": p.name
                                }
                                shutil.copytree(p, tp.joinpath(p.name))
                        elif p.is_file():
                            if p.name.lower() in ("dockerfile", "docker-compose.yml") or (p.suffix in acccept_suffix and p.name not in ("setup.py", "LICENSE", "README.md", "CHANGELOG.md")):
                                nameinfo = p.name.split(".")
                                components[nameinfo[0]] = {
                                    "source": f"{p.name}.jinja",
                                    "description": "",
                                    "default_path": p.name
                                }
                                shutil.copyfile(p, tp.joinpath(p.name))

                def sc(p: Path) -> None:
                    with open(p, encoding="utf-8") as f:
                        content = f.read()
                    for partten, template_key in trans_keys.items():
                        content = content.replace(partten, "{{ " + template_key + " }}")
                    pt = p.parent.joinpath(f"{p.name}.jinja")
                    if pt.exists():
                        print("名称冲突,保留原命名{p}")
                        with open(p, "w", newline="", encoding="utf-8") as fw:
                            fw.write(content)
                    else:
                        with open(pt, "w", newline="", encoding="utf-8") as fw:
                            fw.write(content)
                        os.remove(p)

                iter_dir_to_end(
                    tp,
                    match=lambda p: p.name.lower() in ("dockerfile", "docker-compose.yml") or (p.suffix in acccept_suffix and p.name not in ("setup.py", "LICENSE", "README.md", "CHANGELOG.md")),
                    skip_dir=lambda p: p.name in (pmfpconfig["python_local_env_dir"], pmfpconfig["default_unittest_doc_dir"], pmfpconfig["default_typecheck_doc_dir"]) or p.name in except_dir,
                    skip_dir_handdler=lambda p: shutil.rmtree(p, onerror=remove_readonly),
                    fail_cb=lambda p: os.remove(p),
                    succ_cb=sc)
            except Exception as e:
                warnings.warn(str(e))
            else:
                shutil.copytree(tp, template_dir)

        tempdir(cwdp, tempcallback)

        template_info["components"] = components
        # print(json.dumps(template_info, ensure_ascii=False, indent=4))
        with open(template_dir.joinpath(pmfpconfig["template_config_name"]), "w", encoding="utf-8") as fw:
            json.dump(template_info, fw, indent=4)
        print("转换完成")


project_as_temp = project.regist_sub(AsTemp)
