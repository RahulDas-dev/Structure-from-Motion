"""Module Contains Helper Functions"""

import os


def base_name_converter(filename: str) -> str:
    baseName = os.path.basename(filename).split(".")[:-1]
    return ".".join(baseName) if isinstance(baseName, list) else baseName
