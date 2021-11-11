"""Module Defines Data object."""

import os
from typing import ClassVar

from sfm.utility.helper import base_name_converter


class Data(object):
    """Class Defines Data Object."""

    __name: ClassVar[str]
    __height: ClassVar[int]
    __width: ClassVar[int]

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
        return base_name_converter(self.__name)

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
