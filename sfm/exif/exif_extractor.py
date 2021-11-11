"""Module Defines EXIF data from Images."""

import json
import logging
import os
from datetime import datetime
from functools import lru_cache
from typing import Type

from sfm.component import Component
from sfm.dataset.dataset import Dataset
from sfm.exif.exif_reader import ExifReader
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ExifExtractor(Component):
    """EXID data Extraction from Images."""

    ___next_component: Type[Component]

    def __init__(self, chainable=False):
        super().__init__("EXIF_EXTRACTION", chainable=chainable)

    @lru_cache(maxsize=16)
    def iscompleted(self, count: int) -> bool:
        """Returns True if EXIF Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if os.path.isfile(self.output_path) is False:
            return False
        return True

    def output_path(self) -> str:
        return os.path.join(self.output_directory_path, self.output_file)

    def move_forward(self, dataset: Type[Dataset]):
        start_time = datetime.now()
        dataset_size = len(dataset)
        exif_data_list = []
        for index in tqdm(range(dataset_size), desc="Exif Extraction : "):
            data = dataset(index)
            exif_data = ExifReader(data.name)
            if exif_data.has_exif_metadat is not True:
                continue
            data.set_height_width(exif_data.img_height, exif_data.img_width)
            exif_data_list.append(exif_data.data_as_dictonary())
        with open(self.output_path, "w") as meta_data_file:
            json.dump(exif_data_list, meta_data_file)
        time_elapsed = datetime.now() - start_time
        logger.info(f"Exif Extraction Time (hh:mm:ss.ms) {time_elapsed}")

    def reload(self, dataset: Type[Dataset]):
        start_time = datetime.now()
        exif_data_list = []
        with open(self.output_path) as meta_data_file:
            exif_data_list = json.load(meta_data_file)
        dataset_size = len(dataset)
        for index in tqdm(range(dataset_size), desc="Exif Data Loading : "):
            data = dataset(index)
            exif_data = list(filter(lambda x: x["name"] == data.name, exif_data_list))[0]
            data.set_height_width(exif_data.img_height, exif_data.img_width)
            exif_data_list.remove(exif_data)
        time_elapsed = datetime.now() - start_time
        logger.info(f"Exif data Loading Time (hh:mm:ss.ms) {time_elapsed}")
