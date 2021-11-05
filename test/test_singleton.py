"""Unittesting Module for singleton decorator."""


import unittest

from sfm.utility.singleton_decorator import singleton


class TestSingletonDecorator(unittest.TestCase):
    """Testing singleton decorator."""

    def test_equality_instantiated_with_different_args(self):
        """Object ID should be euqal."""

        @singleton
        class Myclass:
            def __init__(self, data):
                self.data = data

        obj1 = Myclass(10)
        obj2 = Myclass(13.6)

        self.assertEqual(id(obj1), id(obj2), "Objects Ids are not equal")

    def test_equality_instantiated_with_none(self):
        """Object ID should be euqal when one is inataiated with None."""

        @singleton
        class Myclass:
            def __init__(self, data):
                self.data = data

        obj1 = Myclass(10)
        obj2 = Myclass()

        self.assertEqual(id(obj1), id(obj2), "Objects Ids are not equal")

    def test_classmethod_instance(self):
        """Object ID should be euqal when one is inataiated with classmethod instance."""

        @singleton
        class Myclass:
            def __init__(self, data):
                self.data = data

        obj1 = Myclass(10)
        obj2 = Myclass.instance()

        self.assertEqual(id(obj1), id(obj2), "Objects Ids are not equal")

    def test_equality_instantiated_when_class_is_Object(self):
        """Object ID should be euqal when one is inataiated with classmethod instance."""

        @singleton
        class Myclass(object):
            def __init__(self, data):
                self.data = data

        obj1 = Myclass(10)
        obj2 = Myclass.instance()

        self.assertEqual(id(obj1), id(obj2), "Objects Ids are not equal")

    def test_instance_method(self):
        """Object methods should work properly."""

        @singleton
        class Myclass(object):
            def __init__(self, data):
                self.data = data

            def incrementdata(self, factor=1):
                self.data = self.data + factor

        obj1 = Myclass(10)
        obj1.incrementdata(5)
        self.assertEqual(obj1.data, 15, "Object values should be equal 15")


if __name__ == "__main__":
    unittest.main()
