import os
from typing import List

import cv2
from sfm.dataset.imageinfo import ImageInfo


class DatasetGenerator:
    """Data Set Loader."""

    __image_dir: str
    __image_list: List[str]
    __index: int
    __size: int

    __slots__ = "__image_dir", "__image_list", "__index", "__size"

    def __init__(self, image_dir: str, extension: str):
        """Dataset Object Initialaztion.

        Populating __images from list of image present in image_dir with
        valid extension matches to __extension
        """
        self.__image_dir = image_dir
        self.__index = 0
        self.__image_list = list(filter(lambda x: x.split(".")[-1] == extension, os.listdir(image_dir)))
        self.__size = len(self.__image_list)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < self.__size:
            file = self.__image_list[self.__index]
            image_path = os.path.join(self.__image_dir, file)
            image = cv2.imread(image_path)
            h, w = image.shape[:2]
            c = 1 if image.ndim == 2 else image.shape[-1]
            img_id = f"IMAGE_{self.__index + 1:03d}"
            return_value = ImageInfo(file=image_path, imgid=img_id, height=h, width=w, channel=c)
            self.__index += 1
            return return_value
        else:
            raise StopIteration


def dataset_generator(image_dir: str, extension: str):
    image_list = list(filter(lambda x: x.split(".")[-1] == extension, os.listdir(image_dir)))
    for index, file in enumerate(image_list):
        image_path = os.path.join(image_dir, file)
        image = cv2.imread(image_path)
        img_id = img_id = f"IMAGE_{index+1:03d}"
        h, w = image.shape[:2]
        c = 1 if image.ndim == 2 else image.shape[-1]
        yield ImageInfo(file=image_path, imgid=img_id, height=h, width=w, channel=c)
