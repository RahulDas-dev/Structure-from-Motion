import os

import cv2
from sfm.dataset.imageinfo import Data, ImageInfo
from sfm.utility import unique_id_generator


class DatasetGenerator:
    """Data Set Loader."""

    __extension: str
    __image_dir: str

    __slots__ = "__extension", "__image_dir"

    def __init__(self, image_dir: str, extension: str):
        """Dataset Object Initialaztion.

        Populating __images from list of image present in image_dir with
        valid extension matches to __extension
        """
        self.__extension = extension
        self.__image_dir = image_dir

        for image_path in os.listdir(image_dir):
            if os.path.basename(image_path).split(".")[-1] != self.__extension:
                continue
            image_path = os.path.join(image_dir, image_path)
            data = ImageInfo(file = image_path, next(data_id_generator))
            self.__images.append(data)


def dataset_generator(image_dir: str, extension: str):
    data_id_generator = unique_id_generator("IMAGE")
    for file in os.listdir(image_dir):
        if file.split(".")[-1] != extension:
            continue
        image_path = os.path.join(image_dir, file)
        image = cv2.imread(image_path)
        img_id = next(data_id_generator)
        h, w = image.shape[:2]
        c = 1 if image.ndim == 2 else image.shape[-1]
        yield ImageInfo(file=image_path, imgid=img_id, height=h, width=w, channel=c )
