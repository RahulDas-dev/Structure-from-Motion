"""Module Contains Helper Functions."""

import os
from datetime import datetime
from typing import Optional, Tuple, Union

# import psutil


def get_file_count(dir_path: str, allowed_extension: Optional[Union[Tuple[str], str]] = None) -> int:
    if os.path.isdir(dir_path) is False:
        return -1
    if allowed_extension is None:
        return len(os.listdir(dir_path))

    if isinstance(allowed_extension, str):
        allowed_extension = [allowed_extension]
    allowed_extension
    images = list(
        filter(
            lambda x: os.path.basename(x).split(".")[-1] in allowed_extension,
            os.listdir(dir_path),
        )
    )
    return len(images)


def unique_exp_id() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def base_name_converter(filename: str) -> str:
    baseName = os.path.basename(filename).split(".")[:-1]
    return ".".join(baseName) if isinstance(baseName, list) else baseName


def unique_id_generator(prefix: str) -> str:
    """Generates unique id, prefixed with  given argument."""
    index = 1
    while index < 999:
        yield f"{prefix}_{index:03d}"
        index += 1
