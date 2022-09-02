"""Module Defines Pair Selection."""

import logging
import os
from functools import lru_cache
from typing import Tuple

from sfm.component import Component
from sfm.config.config import Config
from sfm.dataset.dataset import Dataset
from sfm.dataset.imageinfo import Data
from sfm.exif.exif_loader import ExifLoader

logger = logging.getLogger(__name__)


class PairSelector(Component):
    """BaseFeatureExtractor Class Defination."""

    def __init__(self, chainable: bool = False):
        """Instantiating Component Class."""
        super().__init__("PAIR_SELECTION", chainable=chainable)
        config = Config.getInstance()
        self.__max_distance = config.max_distance
        self.__gps_neighbour = config.gps_neighbour
        self.__time_neightbour = config.time_neightbour
        (exif_dir, exif_path) = config.sub_directory_path("EXIF_EXTRACTION")
        self.exif_meadata_path = os.path.join(exif_dir, exif_path)
        logger.info("Pair Selection initilized")

    @lru_cache(maxsize=16)
    def iscompleted(self, count: int) -> bool:
        """Returns True if SIFT Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if os.path.isfile(self.output_path) is True:
            return True
        return False

    def move_forward(self, dataset: Dataset):
        exif_loder = ExifLoader(self.exif_meadata_path)
        if exif_loder.has_gps_info:
            pair
