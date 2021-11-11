import os
from itertools import combinations
from os import path
from typing import Callable, List, Type, Union

from sfm.dataset.data import Data
from tqdm import tqdm


class Dataset(object):
    """Data Set Loader."""

    __extension: List[str]
    __images: List[Type[Data]]
    __sorted: bool
    __state: str

    __slots__ = ("__extension", "__images", "__sorted", "__state")

    def __init__(self, image_dir: str, extension: Union[str, List[str]]):
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

        self.__images = []
        for file in tqdm(os.listdir(image_dir), desc="Loading Images to Dataset "):
            if os.path.basename(file).split(".")[-1] not in self.__extension:
                continue
            file = os.path.join(image_dir, file)
            data = Data(file)
            self.__images.append(data)

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
        lambda x: int(x.basename.split("_")[-1])
        self.__images.sort(key=sortfunc)
        self.__sorted = True

    def __getitem__(self, index: int) -> str:
        return self.__images[index]

    def getPairs(self) -> List[str]:
        return combinations(self.__images, 2)

    @property
    def getImagesList(self) -> List[str]:
        return list(map(lambda x: x.name, self.__images))
