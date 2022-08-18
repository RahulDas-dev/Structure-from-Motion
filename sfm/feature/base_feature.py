"""Module Defines Base feature Extraction Protocol."""

from typing import Protocol, Tuple

import numpy as np


class FeatureExtractor(Protocol):
    """BaseFeatureExtractor Class Defination."""

    def iscompleted(self) -> bool:
        """Returns True if SIFT Extraction is complete."""
        ...

    def extract_features(self) -> Tuple[np.ndarray, np.ndarray]:
        ...

    def extract_color(self) -> np.ndarray:
        """Extract Color for each KeyPoint."""
        ...

    def save_features(self, image_path: str):
        """Save Images Key Point, Descriptor and Colors."""
        ...
