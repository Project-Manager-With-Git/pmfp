__all__ = ["create_app"]
import os
import sys
from flask import Flask,url_for
from playhouse.db_url import connect
from config import choose_conf
from model import database_proxys
                  # mongo)



def create_app(conf:str)->Flask:
    static_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]+"/static"
    template_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]+"/templates"
    app = Flask(__name__,template_folder = template_folder,static_folder = static_folder)
    conf = choose_conf(conf)
    app.config.from_object(conf)
    db_urls = app.config.get("DATABASE")
    for k,v in db_urls.items():
        if k in database_proxys.keys():
            database_proxys.get(k).initialize(connect(v))
        else:
            print(f"找不到{k}对应的代理")
    #mongo.init_app(app)

    return app
