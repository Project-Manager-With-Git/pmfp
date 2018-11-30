import json
from pmfp.const import (
    JS_ENV_PATH
)
def new_json_package(config):
    if not JS_ENV_PATH.exists():
        with open(str(JS_ENV_PATH), "w") as f:
            content = {
                "name": config["project-name"],
                "version": config["version"],
                "description": config["description"],
                "author": config["author"],
                "license": config["license"]
            }
            json.dump(content, f)