__all__ = ["TestingConfig"]

from config.config import Config


class TestingConfig(Config):
    SECRET_KEY = "1234567"
    DATABASE = {"accountdb": 'mysql://root:h7wFdCZN2NubZonbXAs1mYUf@114.55.125.148:3306/data_account',
                "baichuandb": 'mysql://root:h7wFdCZN2NubZonbXAs1mYUf@114.55.125.148:3306/data_online'}
    MONGODB_SETTINGS = {'db': 'data_account',
                        'host': '114.55.125.148',
                        'username': 'data_account',
                        'password': 'dataaccount',
                        'port': 27017
                        }
    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
