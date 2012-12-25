def digattr(obj, *args):
    return digattr(getattr(obj, args[0]), *args[1:]) if args else obj


class Query(object):

    def test(self, object):
        raise NotImplemented

    def __and__(self, other):
        return CompoundQuery(self, other)

    def __or__(self, other):
        return CompoundQuery(self, other, op=lambda x, y: x or y)


class CompoundQuery(Query):

    def __init__(self, *args, **kwargs):
        self.queries = args
        self.op = kwargs.pop('op', lambda x, y: x and y)

    def test(self, obj):
        return reduce(self.op, [query.test(obj) for query in self.queries])


class PredicateQuery(Query):

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
        self.key = key
        self.value = value
        frags = key.split('__')
        if len(frags) > 1 and frags[-1] in self.registry:
            self.predicate = self.registry[frags.pop()]
        else:
            self.predicate = self.registry[self.DEFAULT_PREDICATE_NAME]
        self.attrs = frags

    def test(self, obj):
        return self.predicate(digattr(obj, *self.attrs), self.value)


class Q(CompoundQuery):

    def __init__(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(PredicateQuery(k, v))
        super(Q, self).__init__(*args)
