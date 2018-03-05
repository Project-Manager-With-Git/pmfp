import unittest


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearUpModule")


class TestAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        print("instance setUp")

    def tearDown(self):
        print("instance tearDown")

    def test_add_3_4(self):
        self.assertEqual(3 + 4, 7)

    def test_add_3_5(self):
        self.assertEqual(3 + 5, 7)


def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_add_3_4"))
    suite.addTest(TestAdd("test_add_3_5"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
