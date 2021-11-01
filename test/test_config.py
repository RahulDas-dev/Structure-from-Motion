"""Unittesting Module for Config Class."""

import unittest
from test import helper

from sfm.config.config import Config
from sfm.config.defaultConfig import config as default_config


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
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
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir()
        cls.config = Config(config)

    @classmethod
    def tearDownClass(cls):
        cls.config = None


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
        helper.create_temp_output_dir()
        cls.config = Config(config, True)

    @classmethod
    def tearDownClass(cls):
        cls.config = None


if __name__ == "__main__":
    unittest.main()
