======
liquer
======

Query your objects for two cents with Django like ``Q`` objects.

Some Examples
-------------
``Q`` objects help you identify an object if its any attribute conforms your
custom predicate dsl. Let's take a look at the example below::

    from liquer import Q


    class MyClass:
        def __init__(self, foo):
            self.foo = foo

    # Define a query.
    # We expect foo attribute of an object to be 'bar'
    # regardless of case sensivity
    q = Q(foo__iexact='bar')

    # Create one MyClass instance
    my_obj = MyClass(foo='Bar')

    # Test my_obj if it conforms our query object
    assert q(my_obj)  # Evaluates to True

    # We are also free to test any dictionary object
    my_dict = {'foo': 'Bar'}
    assert q(my_dict) 
    
    # Let's fail a test
    my_fail_obj = MyClass(foo='Baz')
    assert q(my_fail_obj)  # Evaluates to False, Throws assertion error


You can tail more attributes using '__' underscores to digg objects::

    >>> from liquer import Q
    >>> my_dict = {'foo': {'bar': {'baz': 1}}}
    >>> q = Q(foo__bar__baz__lte=2)

    >>> q(my_dict)
    True

Also there is chance for applying and/or logics to query couples::

    >>> q = Q(foo__bar__gt=0) & Q(foo__bar__lt=9)  # The same as Q(foo__bar__gt=0, foo__bar__lt=9)
    >>> q({'foo': {'bar': 5}})
    True
    >>> q({'foo': {'bar': 18}})
    False

Let's try ``or`` logic::

    >>> q = Q(foo__bar=3) | Q(foo__bar=5)
    >>> q({'foo': {'bar': 3}})
    True
    >>> q({'foo': {'bar': 5}})
    True
    >>> q({'foo': {'bar': 4}})
    False
    
It's very useful in most cases to register a callback when querying objects::

    >>> q = Q(foo__bar=3) | Q(foo__bar=5)
    >>> q.callback({'foo': {'bar': 3}}, lambda x: 'bar found %s' % x['foo']['bar'])
    'bar found 3'


More is coming soon...

Enjoy!

Licence
-------
Copyright (c) 2012 Kadir Pekel.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
