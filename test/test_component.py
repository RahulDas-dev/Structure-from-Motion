"""Unittesting for abstract Class component,"""
import os
import unittest
from test import helper

from sfm.component import Component
from sfm.config.config import Config
from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS


def setUpModule():
    helper.create_temp_test_dir()


def tearDownModule():
    helper.delete_temp_test_dir()
    # pass


class TestComponent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        config = {
            "dataset_path": helper.DATASET_PATH,
            "output_path": helper.OUTPUT_PATH,
        }
        helper.create_temp_output_dir()
        cls.config = Config(config)

    @classmethod
    def tearDownClass(cls):
        cls.config.disposeInstance()
        cls.config = None

    def test_component_class(self):
        """unit Testing component class."""

        class Mycompent(Component):
            def __init__(self, config, state="EXIF_EXTRACTION"):
                super().__init__(config, state)

            def run(self):
                print("running the Mycomponnet")

        comp = Mycompent(self.config, "EXIF_EXTRACTION")

        self.assertEqual(comp.output_directory_path, os.path.join(helper.OUTPUT_PATH, "exif_data"))
        self.assertTrue(os.path.isdir(comp.output_directory_path))


if __name__ == "__main__":
    unittest.main()
