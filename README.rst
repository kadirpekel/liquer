======
liquer
======

Query your objects for two cents with Django like ``Q`` objects.

Basic Example
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


Example
-------
::

    >>> from liquer import Q

    >>> q = Q(foo__bar='Hello World!') | Q(foo__bar__istartswith='hello',
                                           foo__baz__gt=1)

    >>> q({'foo': {'bar': 'Hello 2013!', 'baz': 2}})
    True

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
