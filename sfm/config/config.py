"""Module Defines Config Desines."""


import json
import os
from datetime import datetime
from typing import Dict, List, Union

from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS

# from sfm.utility.singleton_decorator import singleton


class Config(object):
    """Config Class Defination."""

    __instance = None

    # __state_details: Dict

    @staticmethod
    def getInstance():
        """Static access method."""
        if Config.__instance is None:
            raise Exception("Config Class Has not been instantiated")
        return Config.__instance

    @staticmethod
    def disposeInstance():
        """Static access method."""
        Config.__instance = None

    def __init__(self, config_obj: Dict, re_start: bool = False):
        """Config Object Initialaztion.

        default config and User defined config will be merged
        """
        if Config.__instance != None:
            print(Config.__instance)
            raise Exception("Config Class has been instantiated, kindly use Instance Method")
        if re_start:
            self.__config = config_obj
        else:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
            config_obj["created_at"] = timestamp
            config_obj["exp_id"] = f"SFM_EXPERIMENT_{timestamp}"
            self.__config = {**default_config, **config_obj}
        # self.__state_details = APP_STATE_DETAILS
        Config.__instance = self

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

    @staticmethod
    def valid_state_names() -> List[str]:
        """Returns the list if of Statenames."""
        return list(map(lambda x: x["name"], APP_STATE_DETAILS))

    def sub_directory_path(self, state_name: str) -> str:
        if state_name not in self.valid_state_names():
            raise ValueError(f"State {state_name} is not valid")
        statedict = list(filter(lambda x: x["name"] == state_name, APP_STATE_DETAILS))[0]
        subdir = statedict.get("subdir", None)
        filename = statedict.get("file", None)
        if filename is not None:
            return self.output_path
        else:
            return os.path.join(self.output_path, subdir)
