import sys
import unittest
from pathlib import Path
try:
    from test.test_model._core import Core
except:
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from _core import Core


def setUpModule():
    print("[SetUp Model User to_dict test]")


def tearDownModule():
    print("[TearDown model User to_dict test]")


class ToDictTest(Core):

    def test_user_table_create(self):
        User = self.get_table("User")
        assert User.table_exists() is True
        assert User.select().count() == 4

    def test_user_to_dict(self):
        User = self.get_table("User")
        self.assertDictEqual(
            User.get(User.name == "Li").to_dict(),
            {
                "age": 10,
                "name": "Li"
            }
        )


def to_dict_suite():
    suite = unittest.TestSuite()
    suite.addTest(ToDictTest("test_user_table_create"))
    suite.addTest(ToDictTest("test_user_to_dict"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = to_dict_suite()
    runner.run(test_suite)
