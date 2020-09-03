"""测试pmfp.utils.git_utils模块."""
import unittest
from pathlib import Path
try:
    from pmfp.utils.git_utils import (
        get_latest_commit
    )
except:
    import sys
    from pathlib import Path
    test_dir = str(Path(__file__).resolve().parent.parent.parent)
    if test_dir not in sys.path:
        sys.path.append(test_dir)
    from pmfp.utils.git_utils import (
        get_latest_commit
    )


def setUpModule():
    print("Test [pmfp.utils.git_utils] Set Up")


def tearDownModule():
    print("Test [pmfp.utils.git_utils] Tear Down")


class GetLatestCommitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Test [pmfp.utils.git_utils:get_latest_commit] Set Up")

    @classmethod
    def tearDownClass(cls):
        print("Test [pmfp.utils.git_utils:get_latest_commit] Tear Down")

    def setUp(self):
        print("Test [pmfp.utils.git_utils:get_latest_commit] Case Start")

    def tearDown(self):
        print("Test [pmfp.utils.git_utils:get_latest_commit] Case Done")

    def test_self_latest_commint(self):
        commit = get_latest_commit(r"d:\WorkSpace\Python_Tools\pmfp")
        print(commit)
        assert commit == commit


def submodule_suite():
    suite = unittest.TestSuite()
    suite.addTest(GetLatestCommitTest("test_self_latest_commint"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = submodule_suite()
    runner.run(test_suite)