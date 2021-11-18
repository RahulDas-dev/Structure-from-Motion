"""Module Reads Exif Data."""


import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from sfm.utility.helper import base_name_converter

from exif import Image

logger = logging.getLogger(__name__)


class ExifReader(object):
    """Module Reads Exif Data."""

    __metadata: Dict[str, str]
    __name: str
    __unique_id: str

    __slots__ = ("__metadata", "__name", "__unique_id")

    def __init__(self, image_path: str, unique_id: str):
        with open(image_path, "rb") as image_file:
            self.__metadata = Image(image_file)
        self.__name = base_name_converter(image_path)
        self.__unique_id = unique_id

    @property
    def has_exif_metadat(self) -> bool:
        """Confirm __metadata Exists or not."""
        return self.__metadata.has_exif

    @property
    def exif_version(self) -> str:
        """Extracts Exif version."""
        return self.__metadata.exif_version

    @property
    def height(self) -> int:
        """Extracts Image height."""
        if self.__metadata.get("image_height", None) is not None:
            return self.__metadata.get("image_height")
        return self.__metadata.pixel_y_dimension

    @property
    def width(self) -> int:
        """Extracts Image width."""
        if self.__metadata.get("image_width", None) is not None:
            return self.__metadata.get("image_height")
        return self.__metadata.pixel_x_dimension

    @property
    def make(self) -> str:
        if self.__metadata.make is not None:
            return self.__metadata.make
        return self.__metadata.get("lens_make", None)

    @property
    def model(self) -> str:
        if self.__metadata.model is not None:
            return self.__metadata.model
        return self.__metadata.get("lens_model", None)

    @property
    def orientation(self) -> bool:
        ori = self.__metadata.get("orientation", 1)
        return ori if type(ori) == int and ori != 0 else 1

    @property
    def timestamp(self):
        """Extracts Image timestamp."""
        if self.__metadata.datetime_original is not None:
            return self.__format_date_time(
                self.__metadata.datetime_original,
                self.__metadata.subsec_time_original,
                self.__metadata.get("offset_time_original"),
            )
        elif self.__metadata.datetime_digitized is not None:
            return self.__format_date_time(
                self.__metadata.datetime_digitized,
                self.__metadata.subsec_time_digitized,
                self.__metadata.get("offset_time_digitized"),
            )
        elif self.__metadata.datetime is not None:
            return self.__format_date_time(
                self.__metadata.datetime,
                self.__metadata.subsec_time,
                self.__metadata.get("offset_time"),
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
    def altitude(self) -> Optional[float]:
        if self.__metadata.gps_altitude is not None:
            return self.__metadata.gps_altitude
        return self.__metadata.get("gps_altitude", None)

    @property
    def altitude_ref(self) -> Optional[float]:
        if self.__metadata.gps_altitude_ref is not None:
            return self.__metadata.gps_altitude_ref
        return self.__metadata.get("gps_altitude_ref", None)

    @staticmethod
    def decimal_coords(coords: Tuple[float, float, float], ref: Optional[str]) -> float:
        decimal_degrees = coords[0] + coords[1] / 60.0 + coords[2] / 3600.0
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    @property
    def latitude(self) -> Optional[Tuple[float, float, float]]:
        """Extracts GPS Latitude."""
        if self.__metadata.gps_latitude is not None:
            return self.__metadata.gps_latitude
        return self.__metadata.get("gps_latitude", None)

    @property
    def latitude_ref(self) -> Optional[str]:
        """Extracts GPS Latitude referance."""
        if self.__metadata.gps_latitude_ref is not None:
            return self.__metadata.gps_latitude_ref
        return self.__metadata.get("gps_latitude_ref", None)

    @property
    def longitude(self) -> Optional[Tuple[float, float, float]]:
        """Extracts GPS Longitude."""
        if self.__metadata.gps_longitude is not None:
            return self.__metadata.gps_longitude
        return self.__metadata.get("gps_longitude", None)

    @property
    def longitude_ref(self) -> Optional[str]:
        """Extracts GPS Longitude referance."""
        if self.__metadata.gps_longitude_ref is not None:
            return self.__metadata.gps_longitude_ref
        return self.__metadata.get("gps_longitude_ref", None)

    @property
    def dop(self) -> Optional[str]:
        return self.__metadata.get("gps_dop", None)

    def data_as_dictonary(self) -> Dict:
        return {
            "file": self.__name,
            "image_id": self.__unique_id,
            "exif_version": self.exif_version,
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
                "altitude_ref": self.altitude_ref,
                "latitude": self.latitude,
                "latitude_ref": self.latitude_ref,
                "longitude": self.longitude,
                "longitude_ref": self.longitude_ref,
                "dop": self.dop,
            },
        }
