"""Factory Method for for Feature Extractor."""

from sfm.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from sfm.feature_extractor.sift_extractor import SIFTExtractor


def feature_extractor_object(extractor_type: str, chainable: bool = False) -> BaseFeatureExtractor:
    if extractor_type == "SIFT":
        return SIFTExtractor(chainable)
    else:
        raise Exception(f"extractor_type type {extractor_type} not valid")
