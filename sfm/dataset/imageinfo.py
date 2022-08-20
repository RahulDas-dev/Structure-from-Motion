"""Module Defines Data object."""

import logging
import os
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(init=True, frozen=True)
class ImageInfo:
    """Class Defines Data Object."""

    file: str = field(compare=True)
    imgid: str = field(compare=True)
    height: int = 0
    width: int = 0
    channel: int = 0

    @property
    def basename(self) -> str:
        """Returns name of the without extension."""
        return ".".join(os.path.basename(self.file).split(".")[:-1])

    @property
    def extension(self) -> str:
        """Returns extension of image."""
        return os.path.basename(self.name).split(".")[-1]

    @property
    def image_size(self) -> int:
        """Returns image size in MB."""
        return (self.height * self.width * self.channel) // (1024 * 1024)
