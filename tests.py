import unittest
from liquer import Q


class TestLiquer(unittest.TestCase):

    def testQ(self):
        class A:
            pass

        a = A()
        a.foo = A()
        a.foo.bar = 'Hello World!'
        a.foo.baz = 1

        self.assertTrue(Q(foo__bar='Hello World!').test(a))
        self.assertFalse(Q(foo__bar='hello world!').test(a))
        self.assertTrue(Q(foo__bar__iexact='hello world!').test(a))
        self.assertTrue(Q(foo__baz__lt=2).test(a))
        self.assertTrue(Q(foo__bar='Hello World!', foo__baz=1).test(a))
        self.assertFalse(Q(foo__bar='Hello World!', foo__baz=2).test(a))
        self.assertTrue((Q(foo__bar='Hello World!') | Q(foo__baz=2)).test(a))
        self.assertFalse((Q(foo__bar='Hello World!') & Q(foo__baz=2)).test(a))
        self.assertTrue((Q(foo__bar='Hello World!') & Q(foo__baz=1)).test(a))

if __name__ == '__main__':
    unittest.main()
