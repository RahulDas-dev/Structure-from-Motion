"""Module Defines SFM Engine Class."""


import logging
from datetime import datetime
from typing import ClassVar, Dict

from sfm.component import Component
from sfm.config.config import Config
from sfm.dataset.dataset import Dataset
from sfm.exif.exif_extractor import ExifExtractor

logger = logging.getLogger(__name__)


class AppEngine:

    config: ClassVar[Config]
    restart: ClassVar[bool]
    dataset: ClassVar[Dataset]
    pipe_line_front_component: ClassVar[Component]

    def __init__(self, config_obj: Dict, re_start: bool = False):
        self.config = Config(config_obj, re_start)
        self.restart = re_start
        self.dataset = None
        self.display_info()
        self.build_pipe_line()

    def build_pipe_line(self):
        self.pipe_line_front_component = ExifExtractor(chainable=False)

    def display_info(self):
        logger.info("------------- Config Details -------------")
        print(f"Experiment Name   : { self.config.experiment_id}")
        print(f"Restart Flag      : { self.restart}")
        print(f"Dataset Directory : { self.config.dataset_path}")
        print(f"Output  Directory : { self.config.output_path}")
        print("------------------------------------------")
        print("")

    def load_dataset(self):
        self.dataset = Dataset(self.config.dataset_path, self.config.extension)

    def bootstrap(self):
        start_time = datetime.now()
        self.config.save_config()
        self.load_dataset()
        time_elapsed = datetime.now() - start_time
        logger.info(
            f"Dataset Loading time (hh:mm:ss.ms) {time_elapsed} , Dataset Size {len(self.dataset)}"
        )
        self.pipe_line_front_component.run(self.dataset)
        time_elapsed = datetime.now() - start_time
        logger.info(f"End to End Processing Time (hh:mm:ss.ms) {time_elapsed}")
