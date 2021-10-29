import os
from os import path
from itertools import combinations
from typing import Union, Callable


VALID_EXTENSION: list[str] = ['jpg', 'JPEG', 'png', 'PNG']


class Dataset(object):
    """Data Set Loader."""

    __slots__ = ('__extension', '__images')

    def __init__(self, image_dir: Union[str, list[str]], extension: Union[str, list[str]] = VALID_EXTENSION):
        if image_dir is None or image_dir == []:
            raise ValueError('image_dir is not Valid')
        if isinstance(extension, list):
            if not set(extension).issubset(set(VALID_EXTENSION)):
                raise ValueError('extension is not Valid')
            self.__extension = extension
        else:
            if extension not in VALID_EXTENSION:
                raise ValueError('extension is not Valid')
            self.__extension = [extension]
        if isinstance(image_dir, list):
            if all([path.exists(file) for file in image_dir if path.basename(file).split('.')[1] in self.extension]):
                self.__images = image_dir
            else:
                raise ValueError('image Dir is not valid ')
        else:
            if path.exists(image_dir):
                self.__images = list(filter(lambda x: path.basename(x).split('.')[1] in self.extension, os.listdir(image_dir)))
            else:
                raise ValueError('image List is not valid ')

    def __len__(self) -> int:
        return len(self.__images)

    def sortImages(self, sortfunc: Callable[[str], bool]):
        if not isinstance(sortfunc, Callable[[str], bool]):
            raise ValueError('Sort Function is not valid')
        self.__images.sort(key=sortfunc)

    def __getitem__(self, index: int) -> str:
        return self.__images[index]

    def getPairs(self) -> list[str]:
        return combinations(self.__images, 2)




