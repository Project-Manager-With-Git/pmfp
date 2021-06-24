"""protocol.

用于定义模块支持的可以用于解析的json schema的模式.
"""
TEMPLATE_INFO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["template_type", "components"],
    "additionalProperties": False,
    "properties": {
        "language": {
            "type": "string",
            "description": "模板使用的编程语言",
            "enum": ["py", "cython", "go", "C", "CXX", "js", "md"]
        },
        "mini_language_version": {
            "type": "string",
            "description": "模板使用编程语言的最低版本"
        },
        "description": {
            "type": "string",
            "description": "模板的描述文件"
        },
        "author": {
            "type": "string",
            "description": "模板的作者"
        },
        "template_type": {
            "type": "string",
            "description": "模板库的类型,components表示是组件集合,不能用作模板独立构建项目",
            "enum": ["socket", "GUI", "task", "watcher", "module", "components", "doc"]
        },
        "env": {
            "type": "string",
            "description": "模板推荐的执行环境",
            "enum": ["venv", "conda", "pypy", "gomod", "cmake", "node", "webpack", "http"]
        },
        "requires": {
            "type": "array",
            "title": "r",
            "description": "最小化执行的依赖",
            "items": {
                    "type": "string"
            }
        },
        "test_requires": {
            "type": "array",
            "title": "t",
            "description": "如果有测试部分测试需要的依赖",
            "items": {
                    "type": "string"
            }
        },
        "setup_requires": {
            "type": "array",
            "title": "s",
            "description": "如果有安装部分,安装时的依赖",
            "items": {
                    "type": "string"
            }
        },
        "extras_requires": {
            "type": "array",
            "title": "",
            "description": "扩展的依赖",
            "items": {
                    "type": "string"
            }
        },
        "command": {
            "description": "模板的操作命令,可以是形式为列表的字符串,会被解析为列表",
            "type": "string"
        },
        "test": {
            "type": "object",
            "additionalProperties": False,
            "required": ["default_path", "source"],
            "description": "测试组件名",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "组件在仓库中的存放位置,可以是本地地址`xxx`或者其他外部组件`sss//xxx`"
                },
                "default_path": {
                    "type": "string",
                    "description": "默认放置路径,支持jinja2语法模板"
                }
            }
        },
        "components": {
            "type": "object",
            "description": "模板库中的组件",
            "patternProperties": {
                r"^\w+$": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["default_path", "source"],
                    "description": "组件名对应的配置,组件名为相对模板仓库根目录的相对地址",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "组件在仓库中的存放位置,可以是本地地址`xxx`或者其他外部组件`sss//xxx`"
                        },
                        "description": {
                            "type": "string",
                            "description": "描述组件作用义"
                        },
                        "default_path": {
                            "type": "string",
                            "description": "默认放置路径,支持jinja2语法模板"
                        }
                    }
                }
            }
        },
        "template_keys": {
            "type": "object",
            "description": "模板需要的key",
            "patternProperties": {
                r"^\w+$": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["default"],
                    "description": "键名对应的配置",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "描述键的含义"
                        },
                        "default": {
                            "type": "string",
                            "description": "默认值,如果以`{{ 字段名 }}`包裹则表示使用项目配置中的对应字段,支持指定函数`upper(字段名)/lower(字段名)/Title(字段名)`处理变量"
                        },
                        "ask": {
                            "type": "boolean",
                            "description": "是否在命令行中询问取值"
                        }
                    }
                }
            }
        }
    }
}


PMFP_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cache_dir": {
            "type": "string",
            "description": "cache的缓存位置",
        },
        "default_template_host": {
            "type": "string",
            "description": "模板默认的维护地址",
            "default": "github.com"
        },
        "default_template_namespace": {
            "type": "string",
            "description": "模板默认的维护命名空间",
            "default": "Project-Manager-With-Git"
        },
        "template_config_name": {
            "type": "string",
            "description": "模板的配置文件名",
            "default": ".pmfp_template.json"
        },
        "default_typecheck_doc_dir": {
            "type": "string",
            "description": "类型检测报告的默认文档输出目录",
            "default": "doc_typecheck"
        },
        "default_unittest_doc_dir": {
            "type": "string",
            "description": "单元测试报告的默认文档输出目录",
            "default": "doc_unittest"
        },
        "python": {
            "type": "string",
            "description": "默认使用的python"
        },
        "python_local_env_dir": {
            "type": "string",
            "description": "默认使用的python本地环境的运行环境存放文件"
        }
    }
}
