import os
from os import path
from itertools import combinations
from typing import List, Union, Callable


VALID_EXTENSION: List[str] = ['jpg', 'JPEG', 'png', 'PNG']


class Dataset(object):
    """Data Set Loader."""

    __slots__ = ('__extension', '__images')

    def __init__(self, image_dir: Union[str, List[str]], extension: Union[str, List[str]] = VALID_EXTENSION):
        if image_dir is None or image_dir == []:
            raise ValueError('image_dir Should Valid Directory or List of Images')
        if isinstance(extension, list):
            if not set(extension).issubset(set(VALID_EXTENSION)):
                raise ValueError('extension is not Valid')
            self.__extension = extension
        else:
            if extension not in VALID_EXTENSION:
                raise ValueError('extension is not Valid')
            self.__extension = [extension]
        if isinstance(image_dir, list):
            files = [ file for file in image_dir if path.basename(file).split('.')[1] in self.__extension]
            if len(files) == 0:
                raise FileExistsError(f'Files Extension should be {VALID_EXTENSION}')
            if all([path.exists(file) for file in files]):
                self.__images = image_dir
            else:
                raise FileNotFoundError('All images Files should be Existing')
        else:
            if path.exists(image_dir):
                images = list(filter(lambda x: path.basename(x).split('.')[1] in self.__extension, os.listdir(image_dir)))
                if len(images) == 0:
                    raise FileNotFoundError('image_dir Should Contain Images')  
                self.__images = images       
            else:
                raise NotADirectoryError('image_dir Should Valid Directory')

    def __len__(self) -> int:
        return len(self.__images)

    def sortImages(self, sortfunc: Callable[[str], bool]):
        if not isinstance(sortfunc, Callable[[str], bool]):
            raise ValueError('Sort Function is not valid')
        self.__images.sort(key=sortfunc)

    def __getitem__(self, index: int) -> str:
        return self.__images[index]

    def getPairs(self) -> List[str]:
        return combinations(self.__images, 2)




