"""Unittesting Module for Dataset Class."""

import os
import unittest
from random import shuffle

from sfm.dataset import Dataset
from sfm.defaultConfig import config as default_config

imageDir = "C:/Users/admin/Desktop/codespace/python/Dna_image/images"


class TestDatsetInstantiation(unittest.TestCase):
    """Testing Dataset Class Initialization."""

    def test_create_dataset_with_none(self):
        """Instantiating Dataset Object with None."""
        with self.assertRaises(ValueError) as context:
            _ = Dataset(None)
        self.assertEqual(
            "image_dir should be a valid directory", str(context.exception)
        )


class TestDatsetObject(unittest.TestCase):
    """Testing Dataset Class Methods."""

    @classmethod
    def setUpClass(cls):
        cls.extension = default_config.get("extension")

    def setUp(self) -> None:
        super().setUp()
        self.dataset = Dataset(imageDir)

    def teardown(self):
        self.dataset = None

    def test_length(self):
        images = [
            file
            for file in os.listdir(imageDir)
            if os.path.basename(file).split(".")[-1] in self.extension
        ]
        self.assertEqual(len(self.dataset), len(images))

    def test_getItem(self):
        allFilesvalid = all(
            [os.path.exists(self.dataset[i]) for i in range(len(self.dataset))]
        )
        self.assertEqual(allFilesvalid, True)

    def test_sorted(self):
        self.assertFalse(self.dataset.sorted)
        images = [
            file
            for file in os.listdir(imageDir)
            if os.path.basename(file).split(".")[-1] in self.extension
        ]
        images = [os.path.join(imageDir, file) for file in images]
        shuffle((images))
        sortFunction = lambda x: int(os.path.basename(x).split(".")[0])
        images.sort(key=sortFunction)
        self.dataset.sortImages(sortFunction)
        self.assertListEqual(images, self.dataset.getImagesList)
        self.assertTrue(self.dataset.sorted)


if __name__ == "__main__":
    unittest.main()
