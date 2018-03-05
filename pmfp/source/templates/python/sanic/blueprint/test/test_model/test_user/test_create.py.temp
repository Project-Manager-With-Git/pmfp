import sys
import unittest
from pathlib import Path
path = str(
    Path(__file__).absolute().parent.parent.parent.parent.joinpath(
        "security-center"
    )
)
if path not in sys.path:
    sys.path.append(path)

from App.model import User
try:
    from test.test_model.core import Core
except:
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from core import Core


def setUpModule():
    print("setUp model User Create test")


def tearDownModule():
    print("tearDown model User Create test")


class CreateTest(Core):

    async def _test_user_table_create(self):
        """测试表创建"""
        await self._create_table()
        assert await User.table_exists() is True
        await self._drop_table()

    def test_user_table_create(self):
        self.loop.run_until_complete(self._test_user_table_create())

    async def _test_user_create_single(self):
        """测试创建表中一行数据."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.nickname == self.nickname
        assert user.check_password(self.password)
        assert user.email == self.email
        assert len(user.access_authority) == 1
        assert user.access_authority[0]["name"] == 'security-center'
        await self._drop_table()

    def test_user_create_single(self):
        self.loop.run_until_complete(self._test_user_create_single())

    async def _test_user_create_app(self):
        """测试如果是其他应用调用接口,带着登录应用名时创建用户."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email,
            access_authority="newapp"
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.nickname == self.nickname
        assert user.check_password(self.password)
        assert user.email == self.email
        assert len(user.access_authority) == 2
        access_authority_names = [i["name"] for i in user.access_authority]
        assert 'security-center' in access_authority_names
        assert 'newapp' in access_authority_names
        await self._drop_table()

    def test_user_create_app(self):
        self.loop.run_until_complete(self._test_user_create_app())


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(CreateTest("test_user_table_create"))
    suite.addTest(CreateTest("test_user_create_single"))
    suite.addTest(CreateTest("test_user_create_app"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_suite()
    runner.run(test_suite)
