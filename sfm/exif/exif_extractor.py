"""Module Defines EXIF data from Images."""

import json
import os
from typing import Type

from sfm.component import Component
from sfm.dataset.dataset import Dataset
from sfm.exif.exif_reader import ExifReader


class ExifExtractor(Component):
    """EXID data Extraction from Images."""

    ___next_component: Type[Component]

    def __init__(self, chainable=False):
        super().__init__("EXIF_EXTRACTION", chainable=chainable)

    def iscompleted(self, count: int) -> bool:
        """Returns True if EXIF Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if os.path.isfile(self.output_path) is False:
            return False
        return True

    def run(self, dataset: Type[Dataset]):
        if self.iscompleted(len(dataset)) is False:
            self.move_forward(dataset)
        if self.__chainable:
            self.next_component().run(dataset)

    def output_path(self) -> str:
        return os.path.join(self.output_directory_path, self.output_file)

    def move_forward(self, dataset: Type[Dataset]):
        dataset_size = len(dataset)
        exif_data_list = []
        for index in range(dataset_size):
            data = dataset(index)
            exif_data = ExifReader(data.name)
            if exif_data.has_exif_metadat is not True:
                continue
            data.set_height_width(exif_data.img_height, exif_data.img_width)
            exif_data_list.append(exif_data.data_as_dictonary())
        with open(self.output_path, "w") as meta_data_file:
            json.dump(exif_data_list, meta_data_file)
