"""Singleton Decorator decleration."""


def singleton(class_):
    class WrapperClass(class_):
        __instance = None

        def __new__(class_, *args, **kwargs):
            if WrapperClass.__instance is None:
                WrapperClass.__instance = super(WrapperClass, class_).__new__(class_)
                WrapperClass.__instance.__sealed = False
            return WrapperClass.__instance

        def __init__(self, *args, **kwargs):
            if self.__sealed:
                return
            super(WrapperClass, self).__init__(*args, **kwargs)
            self.__sealed = True

        @classmethod
        def instance(cls):
            if WrapperClass.__instance is None:
                raise Exception("Class Should be initilazed first")
            return WrapperClass.__instance

    WrapperClass.__name__ = class_.__name__
    return WrapperClass
