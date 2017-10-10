from config.default import DefaultConfig
from config.testing import TestingConfig
from config.development import DevelopementConfig
from config.production import ProductionConfig
ENV = {
    "development": DevelopementConfig,
    "testing": TestingConfig,
    "dev": DevelopementConfig,
    "test": TestingConfig,
    "production": ProductionConfig
}


def choose_conf(env):
    return ENV.get(env, DefaultConfig)
