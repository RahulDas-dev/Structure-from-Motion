"""Module Reads Exif Data."""


import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from sfm.utility.helper import base_name_converter

from exif import Image

logger = logging.getLogger(__name__)


class ExifReader(object):
    """Module Reads Exif Data."""

    metadata: Dict[str, str]
    name: str

    def __init__(self, image_path: str):
        with open(image_path, "rb") as image_file:
            self.metadata = Image(image_file)
        self.name = base_name_converter(image_path)

    @property
    def has_exif_metadat(self) -> bool:
        return self.metadata.has_exif

    @property
    def exif_version(self) -> str:
        return self.metadata.exif_version

    @property
    def height(self) -> int:
        if self.metadata.get("image_height", None) is not None:
            return self.metadata.get("image_height")
        return self.metadata.pixel_y_dimension

    @property
    def width(self) -> int:
        if self.metadata.get("image_width", None) is not None:
            return self.metadata.get("image_height")
        return self.metadata.pixel_x_dimension

    @property
    def make(self) -> str:
        if self.metadata.make is not None:
            return self.metadata.make
        return self.metadata.get("lens_make", None)

    @property
    def model(self) -> str:
        if self.metadata.model is not None:
            return self.metadata.model
        return self.metadata.get("lens_model", None)

    @property
    def orientation(self) -> bool:
        ori = self.metadata.get("orientation", 1)
        return ori if type(ori) == int and ori != 0 else 1

    @property
    def timestamp(self):
        if self.metadata.datetime_original is not None:
            return self.__format_date_time(
                self.metadata.datetime_original,
                self.metadata.subsec_time_original,
                self.metadata.get("offset_time_original"),
            )
        elif self.metadata.datetime_digitized is not None:
            return self.__format_date_time(
                self.metadata.datetime_digitized,
                self.metadata.subsec_time_digitized,
                self.metadata.get("offset_time_digitized"),
            )
        elif self.metadata.datetime is not None:
            return self.__format_date_time(
                self.metadata.datetime,
                self.metadata.subsec_time,
                self.metadata.get("offset_time"),
            )
        else:
            return None

    @staticmethod
    def __format_date_time(date_time, sub_sec, offset):
        sub_sec = 0 if sub_sec is None else sub_sec
        datetime_str = "{0:s}.{1:s}".format(date_time, sub_sec)
        datetime_dt = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S.%f")
        if offset is not None:
            hour = -int(str(offset)[0:3])
            minute = int(str(offset)[4:6])
            datetime_dt = datetime_dt - timedelta(hours=hour, minutes=minute)
        return (datetime_dt - datetime(1970, 1, 1)).total_seconds()

    @property
    def altitude(self) -> float:
        if self.metadata.gps_altitude is None:
            return None
        if self.metadata.gps_altitude_ref is None:
            return self.metadata.gps_altitude
        if self.metadata.gps_altitude_ref == 1:
            return -self.metadata.gps_altitude
        return self.metadata.gps_altitude

    @staticmethod
    def decimal_coords(coords: Tuple[float, float, float], ref: Optional[str]) -> float:
        decimal_degrees = coords[0] + coords[1] / 60.0 + coords[2] / 3600.0
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    @property
    def latitude(self) -> float:
        if self.metadata.gps_latitude is None:
            return None
        return self.decimal_coords(self.metadata.gps_latitude, self.metadata.gps_latitude_ref)

    @property
    def longitude(self) -> float:
        if self.metadata.gps_longitude is None:
            return None
        return self.decimal_coords(self.metadata.gps_longitude, self.metadata.gps_longitude_ref)

    def data_as_dictonary(self) -> Dict:
        return {
            "file": self.name,
            "make": self.make,
            "model": self.model,
            "width": self.width,
            "height": self.height,
            # "projection_type": projection_type,
            # "focal_ratio": focal_ratio,
            "orientation": self.orientation,
            "capture_time": self.timestamp,
            "gps": {
                "altitude": self.altitude,
                "latitude": self.latitude,
                "longitude": self.longitude,
            },
        }
