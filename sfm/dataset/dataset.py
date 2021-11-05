import os
from itertools import combinations
from os import path
from typing import Callable, List, Type, Union

from sfm.dataset.data import Data


class Dataset(object):
    """Data Set Loader."""

    __extension: List[str]
    __images: List[Type[Data]]
    __sorted: bool
    __state: str

    __slots__ = ("__extension", "__images", "__sorted", "__state")

    def __init__(self, image_dir: List[str], extension: Union[str, List[str]]):
        """Dataset Object Initialaztion.

        Populating __images from list of image present in image_dir with
        valid extension matches to __extension
        """
        if image_dir is None:
            raise ValueError("image_dir should be a valid directory")
        if isinstance(extension, list):
            self.__extension = extension
        else:
            self.__extension = [extension]

        images = list(
            filter(
                lambda x: path.basename(x).split(".")[-1] in self.__extension,
                os.listdir(image_dir),
            )
        )
        self.__images = [Data(os.path.join(image_dir, file)) for file in images]
        self.__sorted = False
        self.__state = None

    def __len__(self) -> int:
        """Returns the count of images."""
        return len(self.__images)

    @property
    def isSorted(self) -> bool:
        return self.__sorted

    @property
    def state(self) -> bool:
        return self.__state  

    def sortImages(self, sortfunc: Callable[[str], Union[int, float]]):
        self.__images.sort(key=sortfunc)
        self.__sorted = True

    def __getitem__(self, index: int) -> str:
        return self.__images[index]

    def getPairs(self) -> List[str]:
        return combinations(self.__images, 2)

    @property
    def getImagesList(self) -> List[str]:
        return self.__images
