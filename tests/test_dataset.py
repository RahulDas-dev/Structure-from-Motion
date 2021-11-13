"""Unittesting Module for Dataset Class."""

import os
import unittest
from random import shuffle

from sfm.dataset.dataset import Dataset

from tests.helper import (
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

    def setUp(self) -> None:
        super().setUp()
        self.dataset = Dataset(DATASET_PATH, self.extension)

    def teardown(self):
        self.dataset = None

    def test_length(self):
        images = [
            file
            for file in os.listdir(DATASET_PATH)
            if os.path.basename(file).split(".")[-1] in self.extension
        ]
        self.assertEqual(len(self.dataset), len(images))

    def test_getItem(self):
        allFilesvalid = all(
            [os.path.exists(self.dataset[i].name) for i in range(len(self.dataset))]
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


if __name__ == "__main__":
    unittest.main()
