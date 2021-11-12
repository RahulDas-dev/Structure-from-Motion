"""Default Config Object ."""

from typing import Any, Dict

config: Dict[str, Any] = {
    "extension": ["jpg", "jpeg", "JPEG", "png", "PNG"],
    "feature_type": "SIFT",
}

# config = DefaultConfig(extension=["jpg", "jpeg", "JPEG", "png", "PNG"], feature_type="SIFT")
