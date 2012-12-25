from liquer import Q


class B:
    bar = 'Hello World!'
    baz = 1


class A:
    foo = B()


a = A()

q = Q(foo__bar='Hello World!') | Q(foo__bar__istartswith='hello',
                                   foo__baz__gt=1)

assert q(a)

a.foo.bar = 'Hello 2013!'

assert not q(a)

a.foo.baz = 2

assert q(a)
