"""Unittesting Module for Exif Reader."""
import json
import os
import random
import unittest

from sfm.exif.exif_data import ExifData
from sfm.exif.exif_reader import ExifReader
from tests import testtools


def setUpModule():
    testtools.create_temp_test_dir()


def tearDownModule():
    testtools.delete_temp_test_dir()


class TestExifLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        testtools.create_temp_output_dir(True)
        paths = [
            os.path.join(testtools.DATASET_PATH, file)
            for file in os.listdir(testtools.DATASET_PATH)
        ]
        exifList = []
        for index, item in enumerate(paths):
            exif_reader = ExifReader(item, f"IMAGE{index:03d}")
            exifList.append(exif_reader.data_as_dictonary())
        cls.exifjson_path = os.path.join(testtools.OUTPUT_PATH, "meta_data.json")
        with open(testtools.OUTPUT_PATH, "w") as meta_data_file:
            json.dump(exifList, meta_data_file, indent=4)

    @classmethod
    def tearDownClass(cls):
        testtools.clean_dataset_dir()

    def test_exif_reader(self):
        exif_list = []
        with open(self.exifjson_path) as meta_data_file:
            exif_list = json.load(meta_data_file)
        exif_list = list(map(lambda x: ExifData(**x), self.__exif_list))


if __name__ == "__main__":
    unittest.main()
