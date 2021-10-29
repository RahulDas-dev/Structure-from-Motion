import json
import os
from typing import Dict, List, Union

from sfm.defaultConfig import config as default_config

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, os.pardir))
_CONFIG_PATH = os.path.join(_CONFIG_DIR, "config.json")


class Config(object):
    """Config Class Defination."""

    __config: Dict

    def __init__(self, config_path: str = _CONFIG_PATH):
        """Config Object Initialaztion.

        default config and User defined config will be merged
        """
        userConfig = self.__validate_userdefined_config(config_path)
        self.__config = {**default_config, **userConfig}

    def __validate_userdefined_config(self, config_path) -> Dict:
        """Validates The user defined configuration."""
        with open(config_path) as file:
            userConfig = json.load(file)
        # Adding Validation for Directory
        #
        extension = userConfig.get("extension", None)
        if isinstance(extension, list):
            if not set(extension).issubset(set(default_config.get("extension"))):
                raise ValueError("extension is not Valid")
        if isinstance(extension, str):
            if extension not in default_config.get("extension"):
                raise ValueError("extension is not Valid")
        # Adding Validation for Directory
        #
        dataset_path = userConfig.get("dataset_path", None)
        if os.path.isdir(dataset_path):
            images = list(
                filter(
                    lambda x: os.path.basename(x).split(".")[-1]
                    in default_config.get("extension"),
                    os.listdir(dataset_path),
                )
            )
            if len(images) == 0:
                raise FileNotFoundError("dataset_path should contain images")
        else:
            raise NotADirectoryError("dataset_path should be a valid directory")
        return userConfig

    @property
    def extension(self) -> Union[str, List[str]]:
        """Returns the file extension."""
        return self.__config.get("extension")

    @property
    def feature_extractor(self) -> str:
        """Returns the image Local Feature Extractor Type."""
        return self.__config.get("feature_type")
