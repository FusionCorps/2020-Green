def unique(cls):
    """Unique class decorator.

    This decorator will store instances of a *unique* class---classes that
    can only have one instance corresponding to a set of arguments.

    ```python
    from unique import unique

    @unique
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
    instances = {}  # Stores all instances

    # def get_instance(*args, **kwargs):
    #     # frozenset must be used so that dict keys are hashable
    #     if (
    #         cls,
    #         frozen_args := frozenset(args),
    #         frozen_kwargs := frozenset(kwargs),
    #     ) not in instances.keys():
    #         instances[(cls, frozen_args, frozen_kwargs)] = cls(*args, **kwargs)
    #     return instances[(cls, frozen_args, frozen_kwargs)]

    def get_instance(*args, **kwargs):
        if not instances.get(
            (cls, f_args := frozenset(args), f_kwargs := frozenset(kwargs))
        ):
            instances[(cls, f_args, f_kwargs)] = cls(*args, **kwargs)
        return instances[(cls, f_args, f_kwargs)]

    return get_instance


def test_ok():
    @unique
    class Test:
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


# def test_subclass():
#     @unique
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
