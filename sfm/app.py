import logging
from datetime import datetime
from typing import Dict

from sfm.config.config import Config
from sfm.dataset.dataset import Dataset

logger = logging.getLogger(__name__)


class AppEngine:
    def __init__(self, config_obj: Dict, re_start: bool = False):
        self.config = Config(config_obj, re_start)
        self.restart = re_start
        self.dataset = None
        self.display_info()

    def display_info(self):
        logger.info("------------- Config Details -------------")
        logger.info(f"Experiment Name : { self.config.experiment_id}")
        logger.info(f"Restart Flag : { self.restart}")
        logger.info(f"Dataset Directory : { self.config.dataset_path}")
        logger.info(f"Output  Directory : { self.config.output_path}")
        logger.info("------------------------------------------")

    def load_dataset(self):
        self.dataset = Dataset(self.config.dataset_path, self.config.extension)

    def bootstrap(self):
        start_time = datetime.now()
        self.load_dataset()
        time_elapsed = datetime.now() - start_time
        logger.info(f"Dataset Loading time (hh:mm:ss.ms) {time_elapsed}")
        # INSERT YOUR CODE

        time_elapsed = datetime.now() - start_time
        logger.info(f"End to End Processing Time (hh:mm:ss.ms) {time_elapsed}")
