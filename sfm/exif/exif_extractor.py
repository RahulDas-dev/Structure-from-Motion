"""Module Defines EXIF data from Images."""

import os
from typing import Type

from sfm.component import Component
from sfm.dataset.dataset import Dataset


class ExifExtractor(Component):
    """EXID data Extraction from Images."""

    ___next_component: Type[Component]

    def __init__(self, chainable=False):
        super().__init__("EXIF_EXTRACTION", chainable=chainable)

    def iscompleted(self, count: int) -> bool:
        """Returns True if EXIF Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if len(os.listdir(self.output_directory_path)) != count:
            return False
        return True

    def move_forward(self, dataset: Type[Dataset]):
        pass
