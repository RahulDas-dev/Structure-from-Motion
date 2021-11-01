"""Module Defines Config Desines."""


import json
import os
from datetime import datetime
from typing import Dict, List, Union

from sfm.config.default_config import config as default_config


class Config(object):
    """Config Class Defination."""

    __config: Dict

    def __init__(self, config_obj: Dict, re_start: bool = False):
        """Config Object Initialaztion.

        default config and User defined config will be merged
        """
        if re_start:
            self.__config = config_obj
        else:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
            config_obj["created_at"] = timestamp
            config_obj["exp_id"] = f"SFM_EXPERIMENT_{timestamp}"
            self.__config = {**default_config, **config_obj}

    def save_config(self):
        """Saving the config file for Future use, in output_path."""
        output_path = self.__config.get("output_path")
        with open(os.path.join(output_path, "config.json"), "w") as confilg_file:
            json.dump(self.__config, confilg_file)

    @property
    def config_path(self) -> str:
        """Returns the configuration path."""
        return self.__config_path

    @property
    def experiment_id(self) -> str:
        """Returns the Experiment id."""
        return self.__config.get("exp_id")

    @property
    def experiment_creation_date(self) -> str:
        """Returns the Experiment creation Date."""
        return self.__config.get("created_at")

    @property
    def extension(self) -> Union[str, List[str]]:
        """Returns the file extension."""
        return self.__config.get("extension")

    @property
    def dataset_path(self) -> str:
        """Returns the configuration dataset_path."""
        return self.__config.get("dataset_path")

    @property
    def output_path(self) -> str:
        """Returns the configuration output_path."""
        return self.__config.get("output_path")

    @property
    def feature_extractor(self) -> str:
        """Returns the image Local Feature Extractor Type."""
        return self.__config.get("feature_type")
