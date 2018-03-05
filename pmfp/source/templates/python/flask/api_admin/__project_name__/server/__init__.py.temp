from server.default import default
from server.development import development
from server.production import production
from server.testing import testing
from typing import Callable


ENV = {"development": development,
       "dev": development,
       "test": testing,
       "testing": testing,
       "production": production
       }


def choose_server(env: str)->Callable:
    return ENV.get(env, default)


__all__ = ["choose_server"]
