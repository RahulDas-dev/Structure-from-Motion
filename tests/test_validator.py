"""Unittesting for Validator Module."""

import unittest
from datetime import datetime

from sfm.config.validator import validate_userdefined_config

from tests import helper


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
    helper.delete_temp_test_dir()


class TestValidatorFunction(unittest.TestCase):
    """Testing function validate_userdefined_config."""

    def tearDown(self) -> None:
        helper.clean_dataset_dir()

    def test_config_with_invalid_extension_list(self):
        """Config Object with invalid extension list."""
        config = {"extension": ["csv", "tff"]}
        with self.assertRaises(ValueError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_config_with_invalid_extension(self):
        """Config Object with invalid extension."""
        config = {"extension": "rst"}
        helper.write_config_json(config)
        with self.assertRaises(ValueError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual("extension is not Valid", str(context.exception))

    def test_config_with_invalid_dataset_dir(self):
        """Config Object with invalid dataset_path."""
        config = {
            "extension": "PNG",
            "dataset_path": helper.WRONG_DATASET_PATH,
        }
        with self.assertRaises(NotADirectoryError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual(
            "dataset_path directory should be a valid", str(context.exception)
        )

    def test_config_valid_dataset_dir_no_image(self):
        """Config Object with valid dataset_path but no image."""
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.WRONG_DATASET_PATH,
        }
        helper.create_invalid_dataset_dir()
        helper.create_invalid_dataset_files()
        with self.assertRaises(FileNotFoundError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual(
            "dataset_path directory should contain image files", str(context.exception)
        )

    def test_config_none_out_dir(self):
        """Config Object with no output_path."""
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.DATASET_PATH,
        }
        helper.create_valid_dataset_files()
        with self.assertRaises(ValueError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual(
            "Attribute output_path in config.json can not be empty",
            str(context.exception),
        )

    def test_config_invalid_out_dir(self):
        """Config Object with invalid output_path."""
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.WRONG_OUTPUT_PATH,
        }
        with self.assertRaises(NotADirectoryError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual(
            "output_path directory should be a valid", str(context.exception)
        )

    def test_config_with_non_empty_out_dir(self):
        """Config Object with valid non empty output_path."""
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
        }
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir()
        helper.create_invalid_output_files()
        with self.assertRaises(IsADirectoryError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual("output_path directory is not empty", str(context.exception))

    def test_config_with_non_empty_out_dir_restart(self):
        """Config Object with valid non empty output_path and restart enable."""
        timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
            "created_at": timestamp,
            "exp_id": f"SFM_EXPERIMENT_{timestamp}",
        }
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir()
        helper.create_invalid_output_files()
        valid = validate_userdefined_config(config, True)
        self.assertTrue(valid)

    def test_config_with_out_dir_no_permission(self):
        """Config Object with valid output_path, but no Write Permission."""
        config = {
            "extension": ["PNG", "jpg"],
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
        }
        helper.create_valid_dataset_files()
        helper.create_temp_output_dir(False)
        with self.assertRaises(PermissionError) as context:
            _ = validate_userdefined_config(config)
        self.assertEqual(
            "output_path directory should be a Writable", str(context.exception)
        )
