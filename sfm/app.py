"""Module Defines SFM Engine Class."""


import logging
from datetime import datetime
from typing import Dict, Union

from sfm.component import Component
from sfm.config.config import Config
from sfm.dataset.dataset import Dataset
from sfm.exif.exif_extractor import ExifExtractor
from sfm.feature_extractor.feature_extractor_factory import feature_extractor_object

logger = logging.getLogger(__name__)


class AppEngine:

    config: Config
    restart: bool
    dataset: Dataset
    pipe_line_front_component: Component

    def __init__(self, config_obj: Dict[str, Union[str, int, float, bool]]):
        self.config = Config(config_obj)
        self.display_info()
        self.build_pipe_line()

    def build_pipe_line(self):
        """Building Application Pipeline.

        Pipeline First Component --> ExifExtractor --> FeatureExtractor
        """
        self.pipe_line_front_component = ExifExtractor(chainable=True)
        feature_extractor = feature_extractor_object(self.config.feature_extractor, chainable=False)
        self.pipe_line_front_component.set_next_component(feature_extractor)

    def display_info(self):
        """Printing Config and Other info before running App."""
        logger.info("-------------- Config Details --------------")
        print(f"Experiment Name   : { self.config.experiment_id}")
        print(f"Dataset Directory : { self.config.dataset_path}")
        print(f"Output  Directory : { self.config.output_path}")
        print("--------------------------------------------------")
        print("")

    def load_dataset(self):
        """Loading Dataset Object."""
        self.dataset = Dataset(self.config.dataset_path, self.config.extension)

    def bootstrap(self):
        start_time = datetime.now()
        self.config.save_config()
        self.load_dataset()
        time_elapsed = datetime.now() - start_time
        logger.info(f"Dataset Loading time (hh:mm:ss.ms) {time_elapsed}, Dataset Size {self.dataset.image_count}")
        self.pipe_line_front_component.run(self.dataset)
        time_elapsed = datetime.now() - start_time
        logger.info(f"End to End Processing Time (hh:mm:ss.ms) {time_elapsed}")
