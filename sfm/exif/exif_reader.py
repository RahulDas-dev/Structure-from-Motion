"""Module Reads Exif Data."""

import logging
from typing import Dict

import cv2

from exif import Image

logger = logging.getLogger(__name__)


class ExifReader(object):
    """Module Reads Exif Data."""

    metadata: Dict
    img_height: int
    img_width: int

    def __init__(self, image_path: str):
        with open(image_path, "rb") as image_file:
            self.metadata = Image(image_file)
        image = cv2.imread(image_path)
        self.img_height, self.img_width = image.shape[:2]
        image = None

    @property
    def has_exif_metadat(self) -> bool:
        return self.metadata.has_exif

    @property
    def exif_version(self) -> str:
        return self.metadata.exif_version

    @property
    def height(self) -> int:
        return self.metadata.get("image_height", self.img_height)

    @property
    def width(self) -> int:
        return self.metadata.get("image_width", self.img_width)

    @property
    def make(self) -> bool:
        return self.metadata.get("lens_make", None)

    @property
    def model(self) -> bool:
        return self.metadata.get("lens_model", None)

    @property
    def orientation(self) -> bool:
        ori = self.metadata.get("orientation", 1)
        return ori if type(ori) == int and ori != 0 else 1

    def __format_date_time(self, date_stamp, time_stamp):
        pass

    @property
    def timestamp(self):
        time_stamp = self.metadata.get("gps_timestamp", None)
        date_stamp = self.metadata.get("gps_datestamp", None)
        if time_stamp is not None and date_stamp is not None:
            try:
                times_in_sec = self.__format_date_time(date_stamp, time_stamp)
            except (TypeError, ValueError):
                pass

    def data_as_dictonary(self) -> Dict:
        status = f"contains EXIF (version {self.exif_version}) information."
        return {
            "make": self.make,
            "model": self.model,
            "width": self.width,
            "height": self.height,
            # "projection_type": projection_type,
            # "focal_ratio": focal_ratio,
            "orientation": self.orientation,
            # "capture_time": capture_time,
            # "gps": geo,
        }
