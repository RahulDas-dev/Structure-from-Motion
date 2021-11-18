"""Unittesting Module for Exif Reader."""
import os
import random
import unittest

from sfm.config.config import Config
from sfm.exif.exif_reader import ExifReader
from tests import testtools


class TestExifReader(unittest.TestCase):
    def setUp(self) -> None:
        paths = [
            os.path.join(testtools.DATASET_PATH, file)
            for file in os.listdir(testtools.DATASET_PATH)
        ]
        self.imagePaths = random.choices(paths, k=4)

    def tearDown(self) -> None:
        self.imagePaths = []

    def test_exif_reader(self):
        for index, item in enumerate(self.imagePaths):
            exif_reader = ExifReader(item, f"IMAGE{index:03d}")
            exif_data = exif_reader.data_as_dictonary()
            self.assertEqual(exif_reader.exif_version, "0220")
            self.assertIsInstance(exif_data, dict)
            self.assertEqual(
                exif_data.get("file_basename"), os.path.basename(item).split(".")[0]
            )
            self.assertEqual(exif_data.get("image_id"), f"IMAGE{index:03d}")


if __name__ == "__main__":
    unittest.main()
