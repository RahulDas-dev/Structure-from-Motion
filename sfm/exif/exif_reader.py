"""Module Reads Exif Data."""

import logging
from typing import Dict, Tuple

from exif import Image

logger = logging.getLogger(__name__)


class ExifReader(object):
    """Module Reads Exif Data."""

    metadata: Dict

    def __init__(self, image_path: str):
        with open(image_path, "rb") as image_file:
            self.metadata = Image(image_file)

    @property
    def has_exif_metadat(self) -> bool:
        return self.metadata.has_exif

    @property
    def dimention(self) -> Tuple[int, int]:
        return (self.metadata.get("image_height", -1), self.metadata.get("image_width", -1))

    @property
    def maker(self) -> bool:
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
    def timestamp(self) -> bool:
        time_stamp = self.metadata.get("gps_timestamp", None)
        date_stamp = self.metadata.get("gps_datestamp", None)
        if time_stamp is not None and date_stamp is not None:
            try:
                tims_in_sec = self.__format_date_time(date_stamp, time_stamp)
            except (TypeError, ValueError):    

    def             