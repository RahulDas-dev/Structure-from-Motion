"""Module Defines Data object."""

import logging
import os
from typing import Optional

import cv2
from sfm.utility.helper import base_name_converter

logger = logging.getLogger(__name__)


class Data(object):
    """Class Defines Data Object."""

    __name: str
    __height: int
    __width: int
    __channel: int

    __slots__ = ("__name", "__height", "__width", "__channel")

    def __init__(self, name: str):
        self.__name = name
        image = cv2.imread(name)
        self.__height, self.__width = image.shape[:2]
        self.__channel = 1 if image.ndim == 2 else image.shape[-1]

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

    @property
    def image_size(self) -> int:
        return int((self.__height * self.__width * self.__channel) / (1024 * 1024))
