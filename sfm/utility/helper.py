"""Module Contains Helper Functions."""

import os

import psutil


def base_name_converter(filename: str) -> str:
    baseName = os.path.basename(filename).split(".")[:-1]
    return ".".join(baseName) if isinstance(baseName, list) else baseName


def calculate_avaiable_ram() -> int:
    """Returns available memory size in MB."""
    avaiable_memory = psutil.virtual_memory().available
    return int(avaiable_memory / (1024 * 1024))
