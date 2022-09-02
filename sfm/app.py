"""Module Defines SFM Engine Class."""


import json
import logging
import timeit

from sfm.config import Config
from sfm.dataset.dataset import DatasetGenerator
from sfm.utility import unique_exp_id

logger = logging.getLogger(__name__)


class SFMEnginee:

    config_path: str
    config: Config
    experiment_id: str
    restart: bool

    __slots__ = "config", "config_path", "experiment_id", "restart"

    def __init__(self, config_path_: str, exp_id_: str):
        self.config_path = config_path_
        self.experiment_id = unique_exp_id() if exp_id_ is None else exp_id_
        self.restart = False if exp_id_ is None else True
        self.config = None

    def display_info(self):
        """Printing Config and Other info before running App."""
        logger.info(
            f"""
        ------------------------------------------------------
        Experiment ID   : { self.experiment_id}
        {self.config}
        ------------------------------------------------------
        """
        )

    def load_config(self):
        with open(self.config_path) as file:
            config_ = json.load(file)
        self.config = Config(exp_id=self.experiment_id, **config_)

    def load_features(self):
        for item in DatasetGenerator(self.config.dataset_dir, self.config.extension):
            logger.info(item)

    def __call__(self):
        start_time = timeit.default_timer()
        self.load_config()
        self.display_info()
        self.load_features()
        logger.info(f"End to End Processing Time  { timeit.default_timer() - start_time }")
