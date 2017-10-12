import string
import random
from flask_security.utils import encrypt_password
from .db import db as database
from .admin import *
from .targetdb import reflect_db


def build_sample_db(db, app, user_datastore):
    """
    Populate a small db with some example entries.
    """
    print("build_sample_db")
    with app.app_context():
        
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()
        test_admin = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )
        test_user = user_datastore.create_user(
            first_name='User',
            email='user',
            password=encrypt_password('user'),
            roles=[user_role]
        )
        db.session.commit()
        print("build_sample_db done")
    return
