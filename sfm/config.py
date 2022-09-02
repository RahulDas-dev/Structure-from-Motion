"""Module Defines Config Desines."""

import os
from dataclasses import dataclass
from typing import Tuple

from sfm.utility import get_file_count


@dataclass(frozen=True, init=True, repr=False)
class Config:
    """Config Class Defination."""

    # __slots__ = ("dataset_dir", "output_dir", "log_dir", "feature_extractor", "max_keypoint", "allowed_extension")

    exp_id: str
    dataset_dir: str
    output_dir: str
    feature_extractor: str = "SIFT"
    max_keypoint: int = 5000
    extension: str = "jpeg"
    allowed_extension: Tuple[str] = ("jpeg", "jpg", "png", "PNG")
    min_image_count: int = 3

    def __post_init__(self):
        if self.extension not in self.allowed_extension:
            raise RuntimeError("Extensions are not valid")

        if os.path.isdir(self.dataset_dir) is False:
            raise NotADirectoryError("dataset_path directory should be a valid")

        if get_file_count(self.dataset_dir, self.extension) < self.min_image_count:
            raise FileNotFoundError("dataset_path directory should contain image files")

        if os.path.isdir(self.output_dir) is False:
            raise NotADirectoryError("dataset_path directory should be a valid")
        if len(os.listdir(self.output_dir)) > 1:
            raise RuntimeError("output_path directory should be empty")

    @property
    def database_path(self):
        db_file = "db.sfm_{self.exp_id}.sqlite3"
        return os.path.join(self.output_dir, db_file)

    def __repr__(self) -> str:
        return f"""
        Dataset Directory : { self.dataset_dir }
        Output  Directory : { self.output_dir }
        extension         : { self.extension }
        max_keypoint      : { self.max_keypoint }
        """
