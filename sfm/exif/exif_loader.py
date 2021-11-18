"""Module Defines EXIF data loading from exif_data.json."""

import json
import logging
import os
from typing import Dict, List

from sfm.exif.exif_data import ExifData

logger = logging.getLogger(__name__)


class ExifLoader(object):

    __exif_list: List[Dict]
    __exif_data_found: bool

    def __init__(self, metad_data_Path: str):
        self.__exif_list = []
        if os.path.isfile(metad_data_Path) is False:
            self.__exif_data_found = False
            return
        with open(self.output_path) as meta_data_file:
            self.__exif_list = json.load(meta_data_file)
        self.__exif_list = list(map(lambda x: ExifData(**x), self.__exif_list))

    @property
    def isExifDataFound(self) -> bool:
        """Has Exif info across all items."""
        return self.__exif_data_found

    @property
    def has_gps_info(self) -> bool:
        """Has GPS info across all items."""
        return all(list(map(lambda x: x.has_gps_info, self.__exif_list)))

    @property
    def has_capture_time(self) -> bool:
        """Has capture time across all items."""
        return all(list(map(lambda x: x.has_capture_time, self.__exif_list)))
