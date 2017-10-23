
from .debug import DebugEnv
from .local import LocalEnv
from .production import ProductionEnv
from .testing import TestingEnv

ENVS = {
    'debug':DebugEnv,
    "local":LocalEnv,
    'production':ProductionEnv,
    'testing':TestingEnv
}
def env_factory(env):
    return ENVS.get(env,LocalEnv)
