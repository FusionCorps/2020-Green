"""Functionality for a class decorator for unique instances.
"""


class Unique:
    """Unique class decorator.

    This decorator will store instances of a *unique* class---classes that
    can only have one instance corresponding to a set of arguments.

    ```python
    from unique import Unique

    @Unique
    class Test:
        cls_val = 0

        def __init__(self, val):
            self.val = val

    a = Test("a")
    b = Test("b")

    assert a is not b  # Passes

    a_again = Test("a")
    assert a_again is a  # Passes

    print(a.cls_val)  # 0
    print(b.cls_val)  # 0
    ```

    Note:
        Unique classes can inherit from superclasses without problems.

        Performance may be an issue in the future due to the lookups required
        to use a unique class and/or the large keys needed.
    """

    def __init__(self, unique_class):
        self.instances = {}
        self.unique_class = unique_class

    def __call__(self, *args, **kwargs):
        # frozenset used to ensure keys are hashable
        if not self.instances.get(
            (
                self.unique_class,
                f_args := frozenset(args),
                f_kwargs := frozenset(kwargs),
            )
        ):
            # Adds an instance of the wrapped class if it doesn't exist in instances
            self.instances[(self.unique_class, f_args, f_kwargs)] = self.unique_class(
                *args, **kwargs
            )
        return self.instances[(self.unique_class, f_args, f_kwargs)]

    def __getattr__(self, name):
        # Overloaded to access wrapped class attributes
        return object.__getattribute__(self.unique_class, name)


def test_ok():
    @Unique
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

    @Unique
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


# def test_subclass():
#     @Unique
#     class Test:
#         cls_val = 0

#         def __init__(self, val):
#             self.val = val

#     class SubClass(Test):
#         subclass_val = 3

#         def __init__(self, val, super_val):
#             super().__init__(super_val)
#             self.val = val

#     a = SubClass(1, 2)
#     b = SubClass(1, 2)

#     assert a is not b
