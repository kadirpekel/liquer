import unittest
from liquer import Q


class TestLiquer(unittest.TestCase):

    def testQ(self):
        a = {'foo': {'bar': 'Hello World!', 'baz': 1}}
        self.assertTrue(Q(foo__bar='Hello World!')(a))
        self.assertFalse(Q(foo__bar='hello world!')(a))
        self.assertTrue(Q(foo__bar__iexact='hello world!')(a))
        self.assertTrue(Q(foo__baz__lt=2)(a))
        self.assertTrue(Q(foo__bar='Hello World!', foo__baz=1)(a))
        self.assertFalse(Q(foo__bar='Hello World!', foo__baz=2)(a))
        self.assertTrue((Q(foo__bar='Hello World!') | Q(foo__baz=2))(a))
        self.assertFalse((Q(foo__bar='Hello World!') & Q(foo__baz=2))(a))
        self.assertTrue((Q(foo__bar='Hello World!') & Q(foo__baz=1))(a))

if __name__ == '__main__':
    unittest.main()
