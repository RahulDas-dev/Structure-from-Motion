"""Default Config Object ."""

from typing import Any, Dict

config: Dict[str, Any] = {
    "extension": ["jpg", "jpeg", "JPEG", "png", "PNG"],
    "feature_type": "SIFT",
    "max_keypoint_cont": 5000,
    "sift_edge_threshold": 10,
    "sift_peak_threshold": 0.1,
    "max_distance": 0.0,
    "gps_neighbour": 0.0,
    "time_neightbour": 0.0,
}

# config = DefaultConfig(extension=["jpg", "jpeg", "JPEG", "png", "PNG"], feature_type="SIFT")
