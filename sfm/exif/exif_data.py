"""Module Defines EXIF object."""

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass(init=True, repr=True, frozen=True)
class ExifData:
    """Class Defines EXIF DATA Object."""

    file_basename: str
    image_id: str
    exif_version: str
    make: str
    model: str
    width: int
    height: int
    orientation: int
    capture_time: Optional[float]
    altitude: Optional[float]
    altitude_ref: Optional[float]
    latitude: Optional[Tuple[float, float, float]]
    latitude_ref: Optional[str]
    longitude: Optional[Tuple[float, float, float]]
    longitude_ref: Optional[str]
    dop: Optional[float]

    @property
    def has_gps_info(self) -> bool:
        """Has GPS information."""
        if (
            self.latitude is not None
            and self.latitude_ref is not None
            and self.longitude is not None
            and self.longitude_ref is not None
        ):
            return True
        return False

    @property
    def has_capture_time(self) -> bool:
        """Has capture  time."""
        return True if self.capture_time is not None else False

    @staticmethod
    def decimal_coords(coords: Tuple[float, float, float], ref: Optional[str]) -> float:
        """Convert Latitude Longitude to Degree."""
        decimal_degrees = coords[0] + coords[1] / 60.0 + coords[2] / 3600.0
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    @property
    def latitude_in_degree(self) -> Optional[float]:
        """Convert Latitude to Degree."""
        if self.latitude is not None and self.latitude_ref is not None:
            return ExifData.decimal_coords(self.latitude, self.latitude_ref)
        else:
            return None

    @property
    def longitude_in_degree(self) -> Optional[float]:
        """Convert Longitude to Degree."""
        if self.longitude is not None and self.longitude_ref is not None:
            return ExifData.decimal_coords(self.longitude, self.longitude_ref)
        else:
            return None
