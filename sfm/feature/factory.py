"""Factory Method for for Feature Extractor."""

from sfm.feature.base_feature import FeatureExtractor
from sfm.feature.sift_extractor import SIFTExtractor


def extractor_factory(extractor_type: str, chainable: bool = False) -> FeatureExtractor:
    if extractor_type == "SIFT":
        return SIFTExtractor(chainable)
    else:
        raise Exception(f"extractor_type type {extractor_type} not valid")
