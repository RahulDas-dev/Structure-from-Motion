"""Validation Logic for User Defined Config File."""


import os
from typing import Dict

from sfm.config.defaultConfig import config as default_config


def validate_userdefined_config(config_obj: Dict, re_start: bool = False) -> bool:
    """Validates The user defined configuration."""
    #
    # Validation for Extension
    #

    if re_start:
        created_at = config_obj.get("created_at", None)
        exp_id = config_obj.get("exp_id", None)
        if created_at is None or exp_id is None:
            raise Exception("Config_path should be point to old Config file, incase of restart")
        if exp_id.replace("SFM_EXPERIMENT_", "") != created_at:
            raise Exception("Config_path should be point to old Config file, incase of restart")

    extension = config_obj.get("extension", None)
    default_extension = default_config.get("extension")
    if isinstance(extension, list):
        if set(extension).issubset(set(default_extension)) is not True:
            raise ValueError("extension is not Valid")
    if isinstance(extension, str):
        if extension not in default_config.get("extension"):
            raise ValueError("extension is not Valid")
    #
    # Validation for dataset Directory
    #
    dataset_path = config_obj.get("dataset_path", None)
    if os.path.isdir(dataset_path) is not True:
        raise NotADirectoryError("dataset_path directory should be a valid")

    images = list(
        filter(
            lambda x: os.path.basename(x).split(".")[-1] in default_extension,
            os.listdir(dataset_path),
        )
    )
    if len(images) == 0:
        raise FileNotFoundError("dataset_path directory should contain image files")

    #
    # Validating output_path
    #
    output_path = config_obj.get("output_path", None)
    if output_path is None:
        raise ValueError("Attribute output_path in config.json can not be empty")

    if os.path.isdir(output_path) is not True:
        raise NotADirectoryError("output_path directory should be a valid")

    if len(os.listdir(output_path)) > 0 and re_start is False:
        raise IsADirectoryError("output_path directory is not empty")

    if os.access(output_path, os.W_OK) is not True:
        raise PermissionError("output_path directory should be a Writable")

    return True
