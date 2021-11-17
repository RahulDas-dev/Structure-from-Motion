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


def unique_id_generator(prefix: str) -> str:
    """Generates unique id, prefixed with  given argument."""
    index = 0
    prefix = prefix.upper()
    while True:
        index = index + 1 if index < 999 else 1
        yield str(f"{prefix}{index:03d}")
