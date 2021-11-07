"""Module Defines Data object."""

import os

# from typing import Callable, List, Union


class Data(object):
    """Class Defines Data Object."""

    __name: str
    __height: int
    __width: int

    __slots__ = ("__name", "__height", "__width")

    def __init__(self, name: str, height=-1, width=-1):
        self.__name = name
        self.__height = height
        self.__width = width

    @property
    def name(self) -> str:
        return self.__name

    @property
    def basename(self) -> str:
        baseName = os.path.basename(self.__name).split(".")[:-1]
        return ".".join(baseName) if isinstance(baseName, list) else baseName

    @property
    def extension(self) -> str:
        return os.path.basename(self.__name).split(".")[-1]

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def set_height_width(self, height=-1, width=-1):
        self.__height = height
        self.__width = width

    @property
    def isDimessionSet(self):
        return True if self.height > 0 and self.width > 0 else False
