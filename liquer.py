'''Liquer

Query your objects for two cents!

:Licence: MIT
:Author: Kadir Pekel
'''


def digattr(obj, *args):
    '''Function digs and finds any nested attribute value of an object by
    given args path

    :param obj: object to digg
    :param type: object

    :param *args: attribute path
    :param type: list

    :Example::

        >>> class A:
                bar = 'baz'
        >>> class B:
                foo = A()
        >>> b = B()
        >>> digattr(b, 'foo', 'bar')
        'baz'

    '''
    obj = type('obj', (), obj)() if isinstance(obj, dict) else obj
    return digattr(getattr(obj, args[0]), *args[1:]) if args else obj


class Query(object):
    '''Base class for concrete Query classes'''

    def _test(self, obj):
        '''Main entry point for a :py:class:``Query`` object. This method tests
        supplied object against this query. Subclasses have to override this
        method.

        :param obj: subject object
        :param type: object

        '''
        raise NotImplemented()

    def __and__(self, other):
        '''Overrides ``and`` operator and generates a
        :py:class``CompoundQuery`` which supports and/or logics between
        queries.

        :param other: Compound query object
        :param type: :py:class:``Query``

        '''
        return CompoundQuery(self, other)

    def __or__(self, other):
        '''Overrides or operator just like the ``and`` one.

        :param other: Compound query object
        :param type: :py:class:Query

        '''
        return CompoundQuery(self, other, op=lambda x, y: x or y)

    def callback(self, obj, fn):
        '''Tests object with a callback function which is gonna be executed
        once the test succeeds

        :param obj: object to test
        :param type: object

        :param fn: callback function to execute
        :param tyoe: function

        '''
        return fn(obj) if self(obj) else obj

    def __call__(self, obj):
        return self._test(obj)


class CompoundQuery(Query):
    '''Compound query class which tests multiple queries by applying and/or
    logics to them

    '''
    def __init__(self, *args, **kwargs):
        '''Convenient constructor

        :param *args: query list
        :param type: list

        :param op: operator
        :param type: lambda

        '''
        self.queries = args
        self.op = kwargs.pop('op', lambda x, y: x and y)
        super(CompoundQuery, self).__init__()

    def _test(self, obj):
        '''Convenient :py:func:``Query._test`` implementation'''
        return reduce(self.op, [query(obj) for query in self.queries])


class PredicateQuery(Query):
    '''Most notable :py:class:``Query`` implementation which tests objects
    against attribute paths concatanated with double underscores preceding with
    a predicate name.

    :Example::

        >>> pq = PredicateQuery('foo__bar__iexact', 'Baz')
        >>> pq({'foo': {'bar': 'baz'}})
        True

    '''
    DEFAULT_PREDICATE_NAME = 'exact'

    registry = {
        DEFAULT_PREDICATE_NAME: lambda x, y: x == y,
        'lt': lambda x, y: x < y,
        'gt': lambda x, y: x > y,
        'lte': lambda x, y: x <= y,
        'gte': lambda x, y: x >= y,
        'iexact': lambda x, y: x.lower() == y.lower(),
        'startswith': lambda x, y: x.startswith(y),
        'istartswith': lambda x, y: x.lower().startswith(y.lower()),
        'endswith': lambda x, y: x.endswith(y),
        'iendswith': lambda x, y: x.lower().endswith(y.lower()),
        'contains': lambda x, y: x.find(y) >= 0,
        'icontains': lambda x, y: x.lower().find(y.lower()) >= 0,
        'isnull': lambda x, y: x is None if y else x is not None,
        'in': lambda x, y: x in y,
    }

    def __init__(self, key, value):
        '''Convenient constructor

        :param key: attribute path joined with double underscores with a
                    following predicate name
        :param type: str

        :param value: attribute value to test
        :param type: object

        '''
        self.key = key
        self.value = value
        frags = key.split('__')
        if len(frags) > 1 and frags[-1] in self.registry:
            self.predicate = self.registry[frags.pop()]
        else:
            self.predicate = self.registry[self.DEFAULT_PREDICATE_NAME]
        self.attrs = frags
        super(PredicateQuery, self).__init__()

    def _test(self, obj):
        '''Convenient :py:func:``Query._test`` implementation'''
        return self.predicate(digattr(obj, *self.attrs), self.value)


class Q(CompoundQuery):
    '''Convenient :py:class:``PredicateQuery`` like Query implementation
    which generates one or more :py:class:``Query`` instances by the usage of
    keyword arguments. More queries are combined with each other using ``and``
    logic.

    '''
    def __init__(self, **kwargs):
        '''Convenient constructor

        :param **kwargs: keyword arguments consists of key value pairs those
                         passed directly to :py:class:``PredicateQuery``
        :param type: dict

        '''
        super(Q, self).__init__(
            *[PredicateQuery(k, v) for k, v in kwargs.items()])
