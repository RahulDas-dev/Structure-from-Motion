"""Unittesting for abstract Class component,"""
import unittest
from test import helper

from sfm.config.config import Config
from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
    helper.delete_temp_test_dir()


class TestComponent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        config = {
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
        }
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir()
        cls.config = Config(config)

    @classmethod
    def tearDownClass(cls):
        helper.clean_dataset_dir()
        cls.config = None


if __name__ == "__main__":
    unittest.main()
