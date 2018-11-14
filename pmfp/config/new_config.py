import json
from pmfp.const import PMFPRC_PATH, PROJECT_HOME, PMFP_TEMPLATES_HOME
from pmfp.show import show
from pmfp.utils import find_template_path
from .verify import DEFAULT_AUTHOR, LANGUAGE_RANGE, NOT_NAME_RANGE


def new_config(project_name, template=None,language=None):
    config = {
        "project-name": project_name,
        'project-language': language,
        'env': None,
        'project-type': None,
        'template': template,
        'license': "MIT",
        'version': "0.0.1",
        'status': "dev",
        'url': "",
        'author': DEFAULT_AUTHOR,
        'author-email': "",
        'keywords': ["tools"],
        'description': "simple tools",
        'gcc': "gcc",
        'global-python': "python",
        'remote_registry': "",
        "requirement": [],
        "requirement-dev": [],
        "entry": "",
    }
    while True:
        if not project_name:
            while True:
                project_name = input("项目名:")
                project_name = project_name or PROJECT_HOME.name
                if "-" in project_name:
                    project_name.replace("-", "_")
                if project_name in NOT_NAME_RANGE:
                    print(f"名字{project_name}不可以是如下{NOT_NAME_RANGE},请重新输入")
                else:
                    config.update({
                        "project-name": project_name.replace("-","_")
                    })
                    break
        if not language:
            while True:
                project_language = input("项目语言:")
                project_language = project_language.capitalize()
                if project_language not in LANGUAGE_RANGE:
                    print(f"不支持的语言{project_language},目前只支持{LANGUAGE_RANGE},请重新输入")
                else:
                    config.update({
                        "project-language": project_language
                    })
                    break
    
        if config.get("project-language") == "Python":
            default_env = "env"
        elif config.get("project-language")=="Javascript":
            default_env = "node"
        else:
            print("不支持的项目语言")
            return
        env = input("环境:")
        config.update({
            "env": env or default_env
        })

        if template is None:
            while True:
                print("可选的模板有:")
                all_templates = show({
                    "name": None,
                    'category': None,
                    "type": "template",
                    "language": config["project-language"]
                })
                template = input("请输入模板:")
                if template not in all_templates:
                    print("未知的模板,请重新输入")
                else:
                    config.update({
                        "template": template
                    })
                    break
        template_path = find_template_path(config)
        with open(str(template_path)) as f:
            template_info = json.load(f)
        config.update({
            "project-type": template_info["project-type"]
        })

        license_ = input("license:")
        if license_:
            config.update({
                "license": license_
            })
        version = input("project version:")
        if version:
            config.update({
                "version": version
            })
        status = input("project status:")
        if status:
            config.update({
                "status": status
            })
        url = input("url:")
        if url:
            config.update({
                "url": url
            })
        author_ = input("author:")
        if author_:
            config.update({
                "author": author_
            })
        author_email = input("author_email:")
        if author_email:
            config.update({
                "author-email": author_email
            })

        keywords = input("keywords,split by ',':")
        if keywords:
            keywords = [i for i in keywords.split(',')]
            config.update({
                "keywords": keywords
            })

        description = input("description:")
        if description:
            config.update({
                "description": description
            })

        if config["project-type"] == "application" and config["project-language"] == "Python":
            entry = config["project-name"]
            config.update({
                "entry": entry
            })

        return config
