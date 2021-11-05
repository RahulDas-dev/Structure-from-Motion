"""Unittesting Module for Config Class."""
import unittest
from os import pardir, path
from test import helper

from sfm.config.config import Config
from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
    helper.clean_dataset_dir()
    helper.delete_temp_test_dir()


class TestConfigWithNoRestart(unittest.TestCase):
    """Testing Config Object members and methods."""

    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        config = {
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
        }
        helper.create_valid_dataset_files()
        cls.config = Config(config)

    @classmethod
    def tearDownClass(cls):
        cls.config = None

    def test_properties(self):
        """Testing Properies of Config class."""
        self.assertEqual(
            self.config.extension, default_config.get("extension", None), "extension value should be equal to Defauly"
        )
        self.assertEqual(self.config.dataset_path, helper.DATASET_PATH)
        self.assertEqual(self.config.output_path, helper.OUTPUT_PATH)
        self.assertEqual(self.config.feature_extractor, default_config.get("feature_type", None))

    def test_state_sub_directory_path(self):
        """Testing State sub_directory_path."""
        self.assertListEqual(
            self.config.valid_state_names, ["EXIF_EXTRACTION", "FEATURE_EXTRACTION", "MATCHING_FEATURE"]
        )
        subdir_exif = list(filter(lambda x: x["name"] == "EXIF_EXTRACTION", APP_STATE_DETAILS))[0].get("subdir", None)
        subdir = self.config.sub_directory_path("EXIF_EXTRACTION")
        output_dir = path.abspath(path.join(subdir, pardir))
        self.assertEqual(output_dir, helper.OUTPUT_PATH)
        self.assertEqual(subdir, path.join(helper.OUTPUT_PATH, subdir_exif))


class TestConfigWithRestart(unittest.TestCase):
    """Testing Config Object members and methods."""

    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        config = {
            **default_config,
            **{
                "dataset_path": helper.DATASET_PATH,
                "output_path": helper.OUTPUT_PATH,
            },
        }
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        cls.config = Config(config, True)

    @classmethod
    def tearDownClass(cls):
        cls.config = None


if __name__ == "__main__":
    unittest.main()
