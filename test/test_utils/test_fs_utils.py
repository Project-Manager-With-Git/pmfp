"""测试pmfp.utils.fs_utils模块."""
import unittest
from pathlib import Path
try:
    from pmfp.utils.fs_utils import (
        get_abs_path
    )
except:
    import sys
    from pathlib import Path
    test_dir = str(Path(__file__).resolve().parent.parent.parent)
    if test_dir not in sys.path:
        sys.path.append(test_dir)
    from pmfp.utils.fs_utils import (
        get_abs_path
    )


def setUpModule():
    print("Test [pmfp.utils.fs_utils] Set Up")


def tearDownModule():
    print("Test [pmfp.utils.fs_utils] Tear Down")


class GetAbsPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Test [pmfp.utils.fs_utils:get_abs_path] Set Up")

    @classmethod
    def tearDownClass(cls):
        print("Test [pmfp.utils.fs_utils:get_abs_path] Tear Down")

    def setUp(self):
        print("Test [pmfp.utils.fs_utils:get_abs_path] Case Start")

    def tearDown(self):
        print("Test [pmfp.utils.fs_utils:get_abs_path] Case Done")

    def test_self_path(self):
        p = get_abs_path(__file__)
        run_p = Path(".").resolve()
        print(run_p)
        assert p == p


def submodule_suite():
    suite = unittest.TestSuite()
    suite.addTest(GetAbsPathTest("test_self_path"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = submodule_suite()
    runner.run(test_suite)