"""Unittesting for abstract Class component."""


import unittest

from sfm.component import Component
from sfm.config.config import Config

from tests import testtools


def setUpModule():
    testtools.create_temp_test_dir()


def tearDownModule():
    testtools.delete_temp_test_dir()
    # pass


class TestComponent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This will create valid Datset dir and output path, and instantiate a config object."""
        config = {
            "dataset_path": testtools.DATASET_PATH,
            "output_path": testtools.OUTPUT_PATH,
        }
        testtools.create_temp_output_dir()
        cls.config = Config(config)

    @classmethod
    def tearDownClass(cls):
        cls.config.disposeInstance()
        cls.config = None

    def test_component_class(self):
        """unit Testing component class."""

        class Mycompent(Component):
            def __init__(self, state="EXIF_EXTRACTION"):
                super().__init__(state)

            def move_forward(self):
                print("running the Mycomponnet")

            def reload(self, dataset):
                print("reload")

            @property
            def next_component(self):
                return 1

            @property
            def iscompleted(self):
                return True

        comp = Mycompent("EXIF_EXTRACTION")

        self.assertEqual(comp.output_directory_path, testtools.OUTPUT_PATH)
        # self.assertTrue(os.path.isdir(comp.output_directory_path))


if __name__ == "__main__":
    unittest.main()
