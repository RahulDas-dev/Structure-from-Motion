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
            if self.__selead:
                return
            super(WrapperClass, self).__init__(*args, **kwargs)
            self.__selead = True

        @classmethod
        def instance(cls):
            if WrapperClass.__instance is None:
                raise Exception("Class Should be initilazed first")
            return WrapperClass.__instance
