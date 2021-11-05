"""Module Defines Config Desines."""


import json
import os
from datetime import datetime
from typing import Dict, List, Union

from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS
from sfm.utility.singleton_decorator import singleton


@singleton
class Config(object):
    """Config Class Defination."""

    __config: Dict
    __state_details: Dict

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
        self.__state_details = APP_STATE_DETAILS

    def save_config(self):
        """Saving the config file for Future use, in output_path."""
        output_path = self.__config.get("output_path")
        with open(os.path.join(output_path, "config.json"), "w") as confilg_file:
            json.dump(self.__config, confilg_file)

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

    @property
    def valid_state_names(self) -> List[str]:
        """Returns the list if of Statenames."""
        return list(map(lambda x: x["name"], self.__state_details))

    def sub_directory_path(self, state_name: str) -> str:
        if state_name not in self.valid_state_names:
            raise ValueError(f"State {state_name} is not valid")
        statedict = list(filter(lambda x: x["name"] == state_name, self.__state_details))[0]
        subdir = statedict.get("subdir", None)
        filename = statedict.get("file", None)
        if filename is not None:
            return self.output_path
        else:
            return os.path.join(self.output_path, subdir)
