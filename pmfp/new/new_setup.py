from string import Template
from pmfp.const import (
    PMFP_SETUP_TEMP,
    PROJECT_HOME,
)
def new_setup(config,language,name):
    if language == "Python":
        filename = name+".py.temp"
        tempfile = PMFP_SETUP_TEMP.joinpath(filename)
        if not tempfile.exists():
            print(f"找不到{filename}")
        else:
            print("setup.py组件")
            setup_path = PROJECT_HOME.joinpath("setup.py")
            template_content = Template(tempfile.open().read())
            content = template_content.substitute(
                project_name=config["project-name"],
                version=config["version"],
                description=config["description"],
                url=config["url"],
                author=config["author"],
                author_email=config["author-email"],
                license_=config["license"],
                keywords=str(config["keywords"])
            )
            setup_path.open("w").write(content)
            # manifest
            manifest_path = PROJECT_HOME.joinpath("MANIFEST.in")
            manifest_temp = PMFP_SETUP_TEMP.joinpath("MANIFEST.in.temp")
            manifest_content = Template(manifest_temp.open().read())
            content = manifest_content.substitute(
                project_name=config["project-name"]
            )
            manifest_path.open("w").write(content)
    else:
        print("暂时不支持")
        return