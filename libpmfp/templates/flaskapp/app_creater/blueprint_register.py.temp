from flask import Flask,url_for
import blueprints


def blueprint_register(app: Flask)->Flask:
    for i in blueprints.__all__:
        app.register_blueprint(blueprints.__dict__.get(i))
    return app
