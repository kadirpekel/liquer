def digattr(obj, *args):
    return digattr(getattr(obj, args[0]), *args[1:]) if args else obj


class Predicate(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, a, b):
        return self.func(a, b)


class PredicateRegistry(dict):

    def __init__(self, *args, **kwargs):
        for arg in args:
            self[arg.name] = arg
        for k, v in kwargs.items():
            self[k] = Predicate(k, v)


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

    DEFAULT_PREDICATE = Predicate('exact', lambda x, y: x == y)

    registry = PredicateRegistry(
        DEFAULT_PREDICATE,
        Predicate('lt', lambda x, y: x < y),
        Predicate('gt', lambda x, y: x > y),
        Predicate('lte', lambda x, y: x <= y),
        Predicate('gte', lambda x, y: x >= y),

        Predicate('iexact', lambda x, y: x.lower() == y.lower()),
        Predicate('startswith', lambda x, y: x.startswith(y)),
        Predicate('istartswith', lambda x, y: x.lower().startswith(y.lower())),
        Predicate('endswith', lambda x, y: x.endswith(y)),
        Predicate('iendswith', lambda x, y: x.lower().endswith(y.lower())),
        Predicate('contains', lambda x, y: x.find(y) >= 0),
        Predicate('icontains', lambda x, y: x.lower().find(y.lower()) >= 0),

        Predicate('isnull', lambda x, y: x is None if y else x is not None),
        Predicate('in', lambda x, y: x in y),
    )

    def __init__(self, key, value):
        self.key = key
        self.value = value
        frags = key.split('__')
        self.predicate = self.DEFAULT_PREDICATE
        if len(frags) > 1 and frags[-1] in self.registry:
            self.predicate = self.registry[frags.pop()]
        self.attrs = frags

    def test(self, obj):
        return self.predicate(digattr(obj, *self.attrs), self.value)


class Q(CompoundQuery):

    def __init__(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(PredicateQuery(k, v))
        super(Q, self).__init__(*args)
