from liquer import Q


class B:
    bar = 'Hello World!'
    baz = 1


class A:
    foo = B()


q = Q(foo__bar='Hello World!') | Q(foo__bar__istartswith='hello',
                                   foo__baz__gt=1)

print q.test(A())
