"""Module Defines Data object."""

import logging
import os

import cv2
from sfm.utility.helper import base_name_converter

logger = logging.getLogger(__name__)


class Data(object):
    """Class Defines Data Object."""

    __name: str
    __height: int
    __width: int
    __channel: int
    __id: str

    __slots__ = ("__name", "__height", "__width", "__channel", "__id")

    def __init__(self, name: str, data_id: str):
        self.__name = name
        self.__id = data_id
        image = cv2.imread(name)
        self.__height, self.__width = image.shape[:2]
        self.__channel = 1 if image.ndim == 2 else image.shape[-1]

    @property
    def name(self) -> str:
        """Returns absolute path of image."""
        return self.__name

    @property
    def unique_id(self) -> str:
        """Returns id of the image."""
        return self.__id

    @property
    def basename(self) -> str:
        """Returns name of the without extension."""
        return base_name_converter(self.__name)

    @property
    def extension(self) -> str:
        """Returns extension of image."""
        return os.path.basename(self.__name).split(".")[-1]

    @property
    def height(self) -> int:
        """Returns image height."""
        return self.__height

    @property
    def width(self) -> int:
        """Returns image width."""
        return self.__width

    @property
    def image_size(self) -> int:
        """Returns image size in MB."""
        return int((self.__height * self.__width * self.__channel) / (1024 * 1024))
