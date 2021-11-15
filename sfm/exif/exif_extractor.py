"""Module Defines EXIF data from Images."""

import json
import logging
import os
from datetime import datetime
from functools import lru_cache

from sfm.component import Component
from sfm.dataset.dataset import Dataset
from sfm.exif.exif_reader import ExifReader
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ExifExtractor(Component):
    """EXID data Extraction from Images."""

    def __init__(self, chainable: bool = False):
        super().__init__("EXIF_EXTRACTION", chainable=chainable)

    @lru_cache(maxsize=16)
    def iscompleted(self, count: int) -> bool:
        """Returns True if EXIF Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if os.path.isfile(self.output_path) is True:
            return True
        return False

    @property
    def output_path(self) -> str:
        return os.path.join(self.output_directory_path, self.output_file)

    def move_forward(self, dataset: Dataset):
        start_time = datetime.now()
        exif_data_list = []
        for index in tqdm(range(dataset.image_count), desc="Exif Extraction : "):
            data = dataset[index]
            exif_data = ExifReader(data.name)
            if exif_data.has_exif_metadat is not True:
                continue
            exif_data_list.append(exif_data.data_as_dictonary())
        with open(self.output_path, "w") as meta_data_file:
            json.dump(exif_data_list, meta_data_file, indent=4)
        time_elapsed = datetime.now() - start_time
        logger.info(f"Exif Extraction Time (hh:mm:ss.ms) {time_elapsed}")

    def reload(self, dataset: Dataset):
        start_time = datetime.now()
        exif_data_list = []
        with open(self.output_path) as meta_data_file:
            exif_data_list = json.load(meta_data_file)
        for index in tqdm(range(dataset.image_count), desc="Exif Data Loading : "):
            data = dataset[index]
            exif_data = list(filter(lambda x: x["name"] == data.basename, exif_data_list))[0]
            exif_data_list.remove(exif_data)
        time_elapsed = datetime.now() - start_time
        logger.info(f"Exif data Loading Time (hh:mm:ss.ms) {time_elapsed}")
