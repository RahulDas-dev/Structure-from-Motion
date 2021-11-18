"""Unittesting Module for Dataset Class."""

import os
import unittest
from random import shuffle

import cv2
from sfm.dataset.dataset import Dataset

from tests.testtools import (
    DATASET_PATH,
    clean_dataset_dir,
    create_temp_test_dir,
    create_valid_dataset_files,
    delete_temp_test_dir,
)


def setUpModule():
    create_temp_test_dir()
    create_valid_dataset_files()


def tearDownModule():
    clean_dataset_dir()
    delete_temp_test_dir()


class TestDatsetInstantiation(unittest.TestCase):
    """Testing Dataset Class Initialization."""

    def test_create_dataset_with_none(self):
        """Instantiating Dataset Object with None."""
        with self.assertRaises(ValueError) as context:
            _ = Dataset(None, ["jpg", "png", "PNG", "jpeg"])
        self.assertEqual(
            "image_dir should be a valid directory", str(context.exception)
        )


class TestDatsetObject(unittest.TestCase):
    """Testing Dataset Class Methods."""

    @classmethod
    def setUpClass(cls):
        cls.extension = ["jpg", "png", "PNG", "jpeg"]
        cls.dataset = Dataset(DATASET_PATH, cls.extension)

    @classmethod
    def tearDownClass(cls):
        cls.dataset = None

    def test_image_count(self):
        images = [
            file
            for file in os.listdir(DATASET_PATH)
            if os.path.basename(file).split(".")[-1] in self.extension
        ]
        self.assertEqual(self.dataset.image_count, len(images))

    def test_getItem(self):
        allFilesvalid = all(
            [
                os.path.exists(self.dataset[i].name)
                for i in range(self.dataset.image_count)
            ]
        )
        self.assertEqual(allFilesvalid, True)

    def test_sorted(self):
        self.assertFalse(self.dataset.isSorted)
        images = [
            file
            for file in os.listdir(DATASET_PATH)
            if os.path.basename(file).split(".")[-1] in self.extension
        ]
        images = [os.path.join(DATASET_PATH, file) for file in images]
        shuffle((images))
        sortFunction = lambda x: int((os.path.basename(x).split(".")[0]).split("_")[-1])
        sortFunction1 = lambda x: int(x.basename.split("_")[-1])
        images.sort(key=sortFunction)
        self.dataset.sortImages(sortFunction1)
        self.assertListEqual(images, self.dataset.getImagesList)
        self.assertTrue(self.dataset.isSorted)

    def test_image_size(self):
        random_item = self.dataset[2]
        image = cv2.imread(random_item.name)
        height, width = image.shape[:2]
        channel = 1 if image.ndim == 2 else image.shape[-1]
        size = int((height * width * channel) / (1024 * 1024))
        self.assertEqual(self.dataset[2].image_size, size)

    def test_unique_id(self):
        """Each data item of datset should have unique id."""
        ids = set()
        for i in range(self.dataset.image_count):
            ids.add(self.dataset[i].unique_id)
        self.assertEqual(self.dataset.image_count, len(ids))
        ids = list(ids)
        all_should_be_true = all(
            list(map(lambda x: True if "IMAGE" in x else False, ids))
        )
        self.assertTrue(all_should_be_true)


if __name__ == "__main__":
    unittest.main()
