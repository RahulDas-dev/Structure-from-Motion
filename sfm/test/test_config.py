"""Unittesting Module for Config Class."""

import unittest

from sfm.config import Config
from sfm.defaultConfig import config as default_config
from sfm.test import helper


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
    helper.delete_temp_test_dir()


class TestConfigInstantiation(unittest.TestCase):
    """Testing Config Object Initialization."""

    def teardown(self):
        """Deleteing config.json from TEMP_TEST_DIR."""
        helper.delete_config_json()

    def test_instatiate_config_with_invalid_extension_list(self):
        """Instantiating Config Object with invalid extension list."""
        config = {**default_config, **{"extension": ["csv", "tff"]}}
        helper.write_config_json(config)
        with self.assertRaises(ValueError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_instatiate_config_with_invalid_extension(self):
        """Instantiating Config Object with invalid extension."""
        config = {**default_config, **{"extension": "rst"}}
        helper.write_config_json(config)
        with self.assertRaises(ValueError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_instatiate_config_with_invalid_dataset_dir(self):
        """Instantiating Config Object with invalid dataset_path."""
        config = {
            **default_config,
            **{
                "dataset_path": helper.WRONG_DATASET_PATH,
            },
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        helper.create_invalid_dataset_files()
        with self.assertRaises(NotADirectoryError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("dataset_path directory should be a valid", str(context.exception))

    def test_instatiate_config_valid_dataset_dir_no_image(self):
        """Instantiating Config Object with valid dataset_path but no image."""
        config = {
            **default_config,
            **{
                "dataset_path": helper.DATASET_PATH,
            },
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        with self.assertRaises(FileNotFoundError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("dataset_path directory should contain image files", str(context.exception))

    def test_instatiate_config_none_out_dir(self):
        """Instantiating Config Object with no output_path."""
        config = {
            **default_config,
            **{
                "dataset_path": helper.DATASET_PATH,
            },
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        with self.assertRaises(ValueError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("Attribute output_path in config.json can not be empty", str(context.exception))

    def test_instatiate_config_invalid_out_dir(self):
        """Instantiating Config Object with invalid output_path."""
        config = {
            **default_config,
            **{"dataset_path": helper.DATASET_PATH, "output_path": helper.WRONG_OUTPUT_PATH},
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        with self.assertRaises(NotADirectoryError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("output_path directory should be a valid", str(context.exception))

    def test_instatiate_config_with_non_empty_out_dir(self):
        """Instantiating Config Object with valid non empty output_path."""
        config = {
            **default_config,
            **{"dataset_path": helper.DATASET_PATH, "output_path": helper.OUTPUT_PATH},
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir()
        helper.create_invalid_output_files()
        with self.assertRaises(IsADirectoryError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("output_path directory is not empty", str(context.exception))

    def test_instatiate_config_with_out_dir_no_permission(self):
        """Instantiating Config Object with valid output_path, but no Write Permission."""
        config = {
            **default_config,
            **{"dataset_path": helper.DATASET_PATH, "output_path": helper.OUTPUT_PATH},
        }
        helper.write_config_json(config)
        helper.create_temp_dataset_dir()
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir(False)
        with self.assertRaises(PermissionError) as context:
            _ = Config(helper.CONFIG_JSON_PATH)
        self.assertEqual("output_path directory should be a Writable", str(context.exception))


if __name__ == "__main__":
    unittest.main()
