"""Module Defines Config Desines."""

import os
from dataclasses import dataclass, field
from typing import List

from ..utility.helper import get_file_count


@dataclass(frozen=True, slots=True)
class Config:
    """Config Class Defination."""

    dataset_path: str
    output_path: str
    feature_extractor: str = "SIFT"
    max_keypoint_cont: int = 5000
    allowed_extension: List[str] = field(default_factory=lambda: ["jpeg", "jpg", "png", "PNG"])

    def __post_init__(self):
        if os.path.isdir(self.dataset_path) is False:
            raise NotADirectoryError("dataset_path directory should be a valid")

        if get_file_count(self.dataset_path, self.allowed_extension) > 2:
            raise FileNotFoundError("dataset_path directory should contain image files")

        if os.path.isdir(self.output_path) is False:
            raise NotADirectoryError("dataset_path directory should be a valid")
        if len(os.listdir(self.output_path)) > 1:
            raise RuntimeError("output_path directory should be empty")


def ConfigDecoder(object_):
    if "__type__" in object_ and object_["__type__"] == "Config":
        return Config(**object_)
    return object_


studentObj = json.loads(
    '{"__type__": "Student", "rollNumber":1, "name": "Ault kelly", "marks": 78}', object_hook=studentDecoder
)
