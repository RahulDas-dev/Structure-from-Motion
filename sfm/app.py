"""Module Defines SFM Engine Class."""


import json
import timeit
from datetime import datetime

from sfm.config.config import Config


class SFMEnginee:

    config_path: str
    config: Config
    experiment_id: str
    restart: bool

    _slots__ = ("config", "config_path", "experiment_id", "restart")

    @classmethod
    def unique_exp_id():
        return datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    def __init__(self, config_path_: str, exp_id_: str):
        self.config_path = config_path_
        self.experiment_id = self.unique_exp_id() if exp_id_ is None else exp_id_
        self.restart = False if exp_id_ is None else True
        self.config = None

    def display_info(self):
        """Printing Config and Other info before running App."""
        print(
            f"""---------------------{datetime.now()}---------------------
            Experiment ID   : { self.config.experiment_id}
            Dataset Directory : { self.config.dataset_path}
            Output  Directory : { self.config.output_path}
            ------------------------------------------------------"""
        )

    def load_config(self):
        with open(self.config_path) as file:
            config_ = json.load(file)
        self.config = Config(config_)

    def __call__(self):
        start_time = timeit.default_timer()
        self.load_config()
        self.display_info()
        print(f"End to End Processing Time (hh:mm:ss.ms) {start_time - timeit.default_timer()}")
        self.config.disposeInstance()
