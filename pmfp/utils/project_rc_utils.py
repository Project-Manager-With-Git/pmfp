
DEFAULTRCSCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "description": "An address similar to http://microformats.org/wiki/h-card",
  "examples":[
    {
        "project-name": "pmfp",
        "project-type": "tool",
        "remote_registry": "https://github.com/Project-Manager-With-Git/pmfp.git",
        "license": "MIT",
        "version": "4.0.0",
        "url": "https://github.com/Python-Tools/pmfp",
        "author": "hsz",
        "author-email": "hsz1273327@gmail.com",
        "keywords": ["tools", "project_manager"],
        "description": "a simple package manager for python like npm.",
        "components": [],
        "scripts": {"main":"python main.py"}
    },
  ],
  "type": "object",
  "properties": {
    "project-name": {
      "type": "string"
    },
    "project-type": {
      "type": "string"
    },
    "remote_registry": {
      "type": "string"
    },
    "license": {
      "type": "string"
    },
    "version": {
      "type": "string"
    },
    "url": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "author-email": {
      "type": "string"
    },
    "keywords": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "components": {
      "type": "string"
    },
    "scripts": {
      "type": "string"
    }
  },
  "required": [ "project-name", "project-type", "version","author","keywords","description" ]
}


def write_rc():
    pass