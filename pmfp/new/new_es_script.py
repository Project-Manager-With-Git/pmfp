import json
from pmfp.const import (
    JS_ENV_PATH
)
def new_es_script(config):
    entry = config["entry"]   
    with open(str(JS_ENV_PATH)) as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w") as f:
        scripts = {
                "run":f"./node_modules/.bin/babel-node {entry}",
                "build": f"./node_modules/.bin/babel es -d lib",
                "test": "./node_modules/.bin/nyc --reporter=text ./node_modules/.bin/mocha --require babel-polyfill --require babel-register"  
            }
        
        if content.get("esdoc"):
            scripts.update(
                {
                    "doc": "./node_modules/.bin/esdoc",
                }
            )

        content.update({
            "scripts": scripts
        })
        json.dump(content, f)
