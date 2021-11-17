"""Module Defines Base feature Extraction Abstarction."""

import os
import pickle
from abc import abstractmethod
from functools import lru_cache
from typing import Tuple

import cv2
import numpy as np
from sfm.component import Component
from sfm.dataset.data import Data
from sfm.dataset.dataset import Dataset


class BaseFeatureExtractor(Component):
    """BaseFeatureExtractor Class Defination."""

    __keyPoint: np.ndarray
    __descriptors: np.ndarray

    def __init__(self, chainable: bool = False):
        """Instantiating Component Class."""
        super().__init__("FEATURE_EXTRACTION", chainable=chainable)

    @lru_cache(maxsize=16)
    def iscompleted(self, count: int) -> bool:
        """Returns True if SIFT Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if len(os.listdir(self.output_directory_path)) == count:
            return True
        return False

    @abstractmethod
    def extract_features(self, imagePath: str) -> Tuple[np.ndarray, np.ndarray]:
        pass

    def extract_color(self, imagePath: str, keypoints: np.ndarray) -> np.ndarray:
        """Extract Color for each KeyPoint."""
        image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
        xs = keypoints[:, 0].round().astype(int)
        ys = keypoints[:, 1].round().astype(int)
        colors = image[ys, xs]
        if image.shape[2] == 1:
            colors = np.repeat(colors, 3).reshape((-1, 3))
        return colors

    def save_features(
        self,
        data: Data,
        keypoints: np.ndarray,
        descriptor: np.ndarray,
        colors: np.ndarray,
    ):
        """Save Images Key Point, Descriptor and Colors."""
        features = {"keypoint": keypoints, "descriptor": descriptor, "color": colors}
        pickle_file_path = os.path.join(
            self.output_directory_path, f"{data.basename}.pickle"
        )
        with open(pickle_file_path, mode="wb") as pkl_file:
            pickle.dump(features, pkl_file)

    def move_forward(self, dataset: Dataset):
        pass
