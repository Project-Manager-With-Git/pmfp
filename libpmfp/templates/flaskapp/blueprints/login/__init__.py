__all__ = ["login"]
from flask import Blueprint, redirect
login = Blueprint('login', __name__,url_prefix="/login")


import blueprints.login.index
import blueprints.login.logout
import blueprints.login.add_account
import blueprints.login.change_password
