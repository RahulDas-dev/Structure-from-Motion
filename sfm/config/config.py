"""Module Defines Config Desines."""


import json
import os
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from sfm.config.default_config import config as default_config
from sfm.state import APP_STATE_DETAILS


class Config(object):
    """Config Class Defination."""

    __instance: ClassVar = None

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

    def __init__(self, config_obj: Dict[str, Any]):
        """Config Object Initialaztion.

        default config and User defined config will be merged
        """
        if Config.__instance is not None:
            print(Config.__instance)
            raise Exception("Config Class has been instantiated, kindly use Instance Method")
        timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        config_obj["created_at"] = timestamp
        config_obj["exp_id"] = f"SFM_EXPERIMENT_{timestamp}"
        self.__config = {**default_config, **config_obj}
        # self.__state_details = APP_STATE_DETAILS
        Config.__instance = self

    def save_config(self):
        """Saving the config file for Future use, in output_path."""
        output_path: str = self.__config.get("output_path")
        with open(os.path.join(output_path, "config.json"), "w") as confilg_file:
            json.dump(self.__config, confilg_file, indent=4, sort_keys=True)

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
    def max_keypoint_cont(self) -> int:
        """Returns the max_keypoint_cont."""
        return int(self.__config.get("max_keypoint_cont"))

    @property
    def sift_edge_threshold(self) -> int:
        """Returns the sift_edge_threshold."""
        return int(self.__config.get("sift_edge_threshold"))

    @property
    def sift_peak_threshold(self) -> float:
        """Returns the sift_peak_threshold."""
        return float(self.__config.get("sift_peak_threshold"))

    @property
    def max_distance(self) -> float:
        """Returns the minimum physical distance beween two image."""
        return float(self.__config.get("max_distance", 0.0))

    @property
    def gps_neighbour(self) -> float:
        """Returns the minimum physical distance beween two image."""
        return float(self.__config.get("gps_neighbour", 0.0))

    @property
    def time_neightbour(self) -> float:
        """Returns the time gap pbeween two image captures."""
        return float(self.__config.get("time_neightbour", 0.0))

    @staticmethod
    def valid_state_names() -> List[str]:
        """Returns the list if of Statenames."""
        return list(map(lambda x: x["name"], APP_STATE_DETAILS))

    def sub_directory_path(self, state_name: str) -> Tuple[str, Optional[str]]:
        """Determine Subdirectory Path for Given State."""
        if state_name not in self.valid_state_names():
            raise ValueError(f"State {state_name} is not valid")
        statedict = list(filter(lambda x: x["name"] == state_name, APP_STATE_DETAILS))[0]
        subdir: Optional[str] = statedict.get("subdir", None)
        filename: Optional[str] = statedict.get("file", None)
        if filename is not None:
            return (self.output_path, filename)
        else:
            return (os.path.join(self.output_path, subdir), None)
