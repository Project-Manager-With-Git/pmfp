import json
from pmfp.const import (
    JS_ENV_PATH
)


def new_es_script(config):
    entry = config["entry"]
    with open(str(JS_ENV_PATH), encoding="utf-8") as f:
        content = json.load(f)
        old_scripts = content.get("scripts")
    with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
        if config.get("env") == "node":
            default_script = {
                "start": f"./node_modules/.bin/babel-node {entry}",
                "build": f"./node_modules/.bin/babel es -d lib",
                "test": "./node_modules/.bin/nyc --reporter=text ./node_modules/.bin/mocha --require babel-polyfill --require babel-register"
            }
        elif config.get("env") == "webpack":
            default_script = {
                "start": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.dev.js",
                "serv:dev": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.dev.js",
                "serv:test": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.test.js",
                "serv:prod": "./node_modules/.bin/webpack-dev-server --open --config env/webpack.config.prod.js",
                "build": "./node_modules/.bin/webpack --config env/webpack.config.prod.js",
                "build:dev": "./node_modules/.bin/webpack --config env/webpack.config.dev.js",
                "build:test": "./node_modules/.bin/webpack --config env/webpack.config.test.js",
                "build:prod": "./node_modules/.bin/webpack --config env/webpack.config.prod.js",
                "test": "./node_modules/.bin/nyc --reporter=text ./node_modules/.bin/mocha --require babel-polyfill --require babel-register"
            }
        elif config.get("env") == "vue":
            default_script = {
            }
        else:
            default_script = {
            }
        if old_scripts:
            scripts = old_scripts.update(default_script)
        else:
            scripts = default_script
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
