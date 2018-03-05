import sys
import asyncio
import unittest
from unittest import mock
from pathlib import Path
from aioorm.utils import AioDbFactory

path = str(
    Path(__file__).absolute().parent.parent.parent.joinpath(
        "security-center"
    )
)
if path not in sys.path:
    sys.path.append(path)

path = str(
    Path(__file__).absolute().parent.parent.parent
)
if path not in sys.path:
    sys.path.append(path)
from testconfig import DBURI
from App.model import db, User


class Core(unittest.TestCase):
    # 初始化数据库和连接
    @classmethod
    def setUpClass(cls):
        database = AioDbFactory(DBURI)
        database.salt = "qwe"
        cls.nickname = 'huangsizhe'
        cls.password = '12345'
        cls.email = "hsz1273327@gmail.com"
        db.initialize(database)
        cls.loop = asyncio.new_event_loop()
        cls.db = db
        asyncio.set_event_loop(cls.loop)
        print("setUp model test context")

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()
        print("tearDown model test context")

    async def _create_table(self):
        """创建表."""
        await self.db.connect(self.loop)
        await self.db.create_tables([User], safe=True)

    async def _drop_table(self):
        """删除表."""
        await db.drop_tables([User], safe=True)
        await db.close()
