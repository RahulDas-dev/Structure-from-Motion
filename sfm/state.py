"""This Module Defines State of a Application."""


APP_STATE_DETAILS = [
    {"name": "EXIF_EXTRACTION", "subdir": "exif_data"},
    {"name": "FEATURE_EXTRACTION", "subdir": "feature_data"},
    {"name": "MATCHING_FEATURE", "subdir": "matching_data"},
]

APP_STATE_NAMES = list(map(lambda x: x["name"], APP_STATE_DETAILS))
