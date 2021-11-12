"""Module Defines Data object."""

import os
from typing import Optional

from sfm.utility.helper import base_name_converter


class Data(object):
    """Class Defines Data Object."""

    __name: str
    __height: int
    __width: int

    __slots__ = ("__name", "__height", "__width")

    def __init__(self, name: str, height: int = -1, width: int = -1):
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

    def set_height_width(self, height: int = -1, width: int = -1):
        self.__height = height
        self.__width = width

    @property
    def isDimessionSet(self):
        return True if self.height > 0 and self.width > 0 else False

    @property
    def size(self) -> Optional[int]:
        if self.__height == -1 and self.__width == -1:
            return None
        return (self.__height * self.__width * 4) / (1024 * 1024)
