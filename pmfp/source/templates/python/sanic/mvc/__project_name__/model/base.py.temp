"""model基类."""
from peewee import Proxy
from aioorm import AioModel
db = Proxy()

class BaseModel(AioModel):
    """model的基类."""
    class Meta:
        database = db