import logging
from typing import Dict

from sfm.config.config import Config

# logging.basicConfig(format="%(asctime)s : %(name)s -- %(message)s", datefmt="%I:%M:%S %p", level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AppEngine:
    def __init__(self, config_obj: Dict, re_start: bool = False):
        self.config = Config(config_obj, re_start)
        self.restart = re_start
        self.display_info()

    def display_info(self):
        logger.info("------------- Config Details -------------")
        logger.info(f"Experiment Name : {self.config.experiment_id}")
        logger.info(f"Restart Flag : {self.restart}")
        logger.info(f"Dataset Directory : {self.config.dataset_path}")
        logger.info(f"Output  Directory : {self.config.output_path}")
        logger.info("------------------------------------------")

    def bootstrap(self):
        logger.info("Running The Engine")
        print("Running The Engine")
