"""Unittesting Module for Config Class."""

import unittest

from sfm.config import Config
from sfm.defaultConfig import config as default_config
from sfm.test.helper import (
    CONFIG_JSON_PATH,
    TEMP_TEST_DIR,
    create_temp_test_dir,
    delete_config_json,
    delete_temp_test_dir,
    write_config_json,
)


def setUpModule():
    create_temp_test_dir()


def tearDownModule():
    delete_temp_test_dir()


class TestConfigInstantiation(unittest.TestCase):
    """Testing Config Object Initialization."""

    def teardown(self):
        """Deleteing config.json from TEMP_TEST_DIR."""
        delete_config_json()

    def test_instatiate_with_invalid_extension_list(self):
        """Instantiating Config Object with invalid extension list."""
        config = {**default_config, **{"extension": ["csv", "tff"]}}
        write_config_json(config)
        with self.assertRaises(ValueError) as context:
            _ = Config(CONFIG_JSON_PATH)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_instatiate_with_invalid_extension(self):
        """Instantiating Config Object with invalid extension."""
        config = {**default_config, **{"extension": "rst"}}
        write_config_json(config)
        with self.assertRaises(ValueError) as context:
            _ = Config(CONFIG_JSON_PATH)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_instatiate_with_invalid_directory(self):
        """Instantiating Config Object with invalid dataset_path."""
        config = {
            **default_config,
            **{
                "dataset_path": "C:/desktop/image_dir",
            },
        }
        write_config_json(config)
        with self.assertRaises(NotADirectoryError) as context:
            _ = Config(CONFIG_JSON_PATH)
        self.assertEqual(
            "dataset_path should be a valid directory", str(context.exception)
        )

    def test_create_dataset_valid_directory_no_image(self):
        """Instantiating Config Object with valid dataset_path but no image."""
        config = {
            **default_config,
            **{
                "dataset_path": TEMP_TEST_DIR,
            },
        }
        write_config_json(config)
        with self.assertRaises(FileNotFoundError) as context:
            _ = Config(CONFIG_JSON_PATH)
        self.assertEqual("dataset_path should contain images", str(context.exception))


if __name__ == "__main__":
    unittest.main()
