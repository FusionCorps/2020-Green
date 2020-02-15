"""Functionality for a class decorator for unique instances.
"""

from functools import lru_cache, wraps
from inspect import signature


def unique(unique_class):
    """Class decorator for unique classes.

    The unique decorator caches each instance of a class that corresponds to
    unique arguments. This is useful to prevent multiple instances of one class
    being created with the same arguments.

    Example:
        ```python
        from fusion.unique import unique

        @unique
        class Test:
            cls_val = 0

            def __init__(self, val):
                self.val = val

        a = Test(1)
        b = Test(2)

        assert a is not b

        a_again = Test(1)

        assert a_again is a
        ```

    Note:
        This is essential when dealing with robotPy segfaults, which occur when
        a Python object that is managed from C gets garbage collected and
        subsequently accessed (invalid). The `unique` decorator ensures there is
        always at least one reference to a given instance and set of arguments.

        DO NOT EVER USE A `@unique` CLASS AS A BASE CLASS!
    """

    def sort_args(func: callable):
        """Sorts arguments before passing them to the wrapped function.

        Args:
            func (callable): callable to be wrapped
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = signature(
                unique_class.__init__
            )  # Needs to get sig of class constructor to be useful

            bound_arguments = sig.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            return func(
                *bound_arguments.args, **dict(sorted(bound_arguments.kwargs.items()))
            )

        return wrapper

    class Unique(unique_class):
        @sort_args
        @lru_cache(maxsize=None)
        def __new__(cls, *args, **kwargs):
            return super().__new__(cls)

    return Unique


# Pytest Tests


def test_ok():
    @unique
    class Test:
        """
        Hello.
        """

        cls_val = 0

        def __init__(self, val):
            self.val = val

    a = Test("a")
    b = Test("b")

    assert a is not b

    a_again = Test("a")
    b_again = Test("b")

    assert a_again is a
    assert b_again is b

    assert a.val == "a"
    assert b.val == "b"


def test_inheritance():
    class SuperClass:
        superclass_val = 3

        def __init__(self, super_val):
            self.super_val = super_val

    @unique
    class Test(SuperClass):
        cls_val = 0

        def __init__(self, val, super_val):
            super().__init__(super_val)
            self.val = val

    a = Test("a", 2)
    a_diff = Test("a", 3)
    b = Test("b", 3)

    assert a is not b
    assert a_diff is not a and a_diff is not b

    a_again = Test("a", 2)
    b_again = Test("b", 3)

    assert a_again is a
    assert b_again is b

    assert a.val == "a"
    assert b.val == "b"

    assert a.superclass_val == 3
    assert a.super_val == 2


def test_subclass():
    @unique
    class Test:
        cls_val = 0

        def __init__(self, a, time_to_completion=None):
            self.time_to_completion = time_to_completion
            self.a = a

    class SubClass(Test):
        subclass_val = 3

        def __init__(self, val, time_to_completion=None):
            super().__init__(0, time_to_completion=time_to_completion)
            self.val = val

    a = SubClass(1, time_to_completion=2)
    b = SubClass(1, 2)

    d = SubClass(2, 3)

    assert a.subclass_val == 3
    assert a.cls_val == 0

    assert a is b

    assert d is not a


# def test_order():
#     """The same arguments, but in a different order, should still return
#     the same instance."""

#     @unique
#     class Test:
#         cls_val = 0

#         def __init__(self, a, b, c=1, d=2, *args, z=3, x=4, y=5, **kwargs):
#             pass

#     a = Test(-1, 0, 6, 7, 8, x=2, z=3, y=5, f=1, g=2)
#     b = Test(-1, 0, 6, 7, 8, z=3, x=2, g=2, f=1)

#     assert a is b

#     class SubClass(Test):
#         subclass_val = 0

#         def __init__(self, a, b, time=0, **kwargs):
#             super().__init__(-1, 0, 6, 7, 8, x=2, z=3, y=5, f=1, g=2)

#     c = SubClass(1, 2, 3, z=1)
#     d = SubClass(1, 2, z=1)

#     assert c is d
