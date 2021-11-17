"""Validation Logic for User Defined Config File."""


import os
from typing import Any, Dict, List, Optional, Union

from sfm.config.default_config import config as default_config


def validate_userdefined_config(config_obj: Dict[str, Any]) -> bool:
    """Validates The user defined configuration."""
    #
    # Validation for Extension
    #

    extension: Optional[Union[str, List[str]]] = config_obj.get("extension", None)
    default_extension: List[str] = default_config.get("extension")
    if isinstance(extension, list):
        if set(extension).issubset(set(default_extension)) is not True:
            raise ValueError("extension is not Valid")
    if isinstance(extension, str):
        if extension not in default_extension:
            raise ValueError("extension is not Valid")
    #
    # Validation for dataset Directory
    #
    dataset_path: Optional[str] = config_obj.get("dataset_path", None)
    if dataset_path is None:
        raise ValueError("Attribute output_path in config.json can not be empty")

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
    output_path: Optional[str] = config_obj.get("output_path", None)
    if output_path is None:
        raise ValueError("Attribute output_path in config.json can not be empty")

    if os.path.isdir(output_path) is not True:
        raise NotADirectoryError("output_path directory should be a valid")

    if len(os.listdir(output_path)) > 0:
        raise IsADirectoryError("output_path directory is not empty")

    if os.access(output_path, os.W_OK) is not True:
        raise PermissionError("output_path directory should be a Writable")

    return True
