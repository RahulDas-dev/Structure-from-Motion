import logging
from datetime import datetime
from typing import Dict

from sfm.config.config import Config

logger = logging.getLogger(__name__)


class AppEngine:
    def __init__(self, config_obj: Dict, re_start: bool = False):
        self.config = Config(config_obj, re_start)
        self.restart = re_start
        self.display_info()

    def display_info(self):
        logger.info("------------- Config Details -------------")
        logger.info(f"Experiment Name : { self.config.experiment_id}")
        logger.info(f"Restart Flag : { self.restart}")
        logger.info(f"Dataset Directory : { self.config.dataset_path}")
        logger.info(f"Output  Directory : { self.config.output_path}")
        logger.info("------------------------------------------")

    def bootstrap(self):
        start_time = datetime.now()
        # INSERT YOUR CODE
        # INSERT YOUR CODE
        # INSERT YOUR CODE
        time_elapsed = datetime.now() - start_time
        logger.info(f"End to End Processing Time (hh:mm:ss.ms) {time_elapsed}")
