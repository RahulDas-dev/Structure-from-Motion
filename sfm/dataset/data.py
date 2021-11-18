"""Module Defines Data object."""

import logging
import os
from dataclasses import dataclass, field

import cv2
from sfm.utility.helper import base_name_converter

logger = logging.getLogger(__name__)


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Data:
    """Class Defines Data Object."""

    name: str = field(compare=True)
    unique_id: str = field(compare=True)
    height: int = field(init=False)
    width: int = field(init=False)
    channel: int = field(init=False)

    def __post_init__(self):
        """Initilizing Data objects with name and id."""
        image = cv2.imread(self.name)
        height, width = image.shape[:2]
        channel = 1 if image.ndim == 2 else image.shape[-1]
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "channel", channel)

    @property
    def basename(self) -> str:
        """Returns name of the without extension."""
        return base_name_converter(self.name)

    @property
    def extension(self) -> str:
        """Returns extension of image."""
        return os.path.basename(self.name).split(".")[-1]

    @property
    def image_size(self) -> int:
        """Returns image size in MB."""
        return int((self.height * self.width * self.channel) / (1024 * 1024))
