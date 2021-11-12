"""This Module Defines State of a Application."""

from typing import Dict, List

APP_STATE_DETAILS: List[Dict[str, str]] = [
    {"name": "EXIF_EXTRACTION", "file": "exif_data.json"},
    {"name": "FEATURE_EXTRACTION", "subdir": "feature_data"},
    {"name": "MATCHING_FEATURE", "subdir": "matching_data"},
]

APP_STATE_NAMES = list(map(lambda x: x["name"], APP_STATE_DETAILS))
