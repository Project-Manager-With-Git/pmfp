__all__ = ["main"]
from flask import Blueprint, redirect
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "hello"

@main.route('/logout', methods=["POST"])
def logout():
    redirect("/login/logout")

@main.route('/change_password',methods=["POST"] )
def change_password():
    redirect("/login/change_password")

@main.route('/add_account',methods=["POST"] )
def add_account():
    redirect("/login/add_account")
