"""Module Defines SIFT feature Extraction logic."""

import logging
import os
from datetime import datetime
from functools import lru_cache
from typing import Tuple

import cv2
import numpy as np
from sfm.config.config import Config
from sfm.dataset.dataset import Dataset
from sfm.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from tqdm import tqdm

logger = logging.getLogger(__name__)


class SIFTExtractor(BaseFeatureExtractor):
    """EXID data Extraction from Images."""

    def __init__(self, chainable: bool = False):
        """Initilizing Sift with Config and its base class."""
        super().__init__(chainable=chainable)
        config = Config.getInstance()
        self.__edge_threshold = config.sift_edge_threshold
        self.__peak_threshold = config.sift_peak_threshold
        self.__peak_threshold_default = config.sift_peak_threshold
        self.__sift_object = cv2.SIFT_create(
            edgeThreshold=self.__edge_threshold, contrastThreshold=self.__peak_threshold
        )
        self.__max_keypoint_cont = config.max_keypoint_cont
        logger.info(
            f"SIFT initilized with threshold {self.__edge_threshold}, {self.__peak_threshold}"
        )

    @lru_cache(maxsize=16)
    def iscompleted(self, count: int) -> bool:
        """Returns True if SIFT Extraction is complete."""
        if self.is_output_dir_exists is False:
            return False
        if len(os.listdir(self.output_directory_path)) == count:
            return True
        return False

    def reset_parameters(self):
        """Reset Sift Parameters."""
        self.__peak_threshold = self.__peak_threshold_default

    def move_forward(self, dataset: Dataset):
        """Iterate over Dataset and Extracts Keypoint & descriptors & Save in Pickle File."""
        start_time = datetime.now()
        for index in tqdm(range(dataset.image_count), desc="SIFT Extraction : "):
            data = dataset[index]
            key_points, descriptor = self.extract_features(data.name)
            size = key_points[:, 2]
            order = np.argsort(size)
            key_points_sorted = key_points[order, :]
            descriptor_sorted = descriptor[order, :]
            colors_sorted = self.extract_color(data.name, key_points_sorted)
            self.save_features(
                data, key_points_sorted, descriptor_sorted, colors_sorted
            )
        logger.info(f"SIFT Extraction Time (hh:mm:ss.ms) {datetime.now() - start_time}")

    def extract_features(self, imagePath: str) -> Tuple[np.ndarray, np.ndarray]:
        """Modify the sift Parameter and key point detection & descripter Computation."""
        gray_image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        self.reset_parameters()
        while True:
            self.__sift_object = cv2.SIFT_create(
                edgeThreshold=self.__edge_threshold,
                contrastThreshold=self.__peak_threshold,
            )
            key_points = self.__sift_object.detect(gray_image)
            if (
                len(key_points) < self.__max_keypoint_cont
                and self.__peak_threshold > 0.0001
            ):
                self.__peak_threshold = (self.__peak_threshold * 2) / 3
            else:
                break
        key_points, descriptor = self.__sift_object.compute(gray_image, key_points)
        key_points = np.array([(i.pt[0], i.pt[1], i.size, i.angle) for i in key_points])
        return key_points, descriptor

    def reload(self, dataset: Dataset):
        """reloading Dataset Incase rerun."""
        print("Reloaded Dataset SIFT Features")
