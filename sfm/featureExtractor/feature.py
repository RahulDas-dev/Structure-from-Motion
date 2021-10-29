from abc import ABC, abstractmethod
from typing import List, Union, Callable, Type

from sfm.dataset import Dataset

class FeatureExtractor(ABC):

    def __init__(self, dataset: Type[Dataset]):
        self.dataset = dataset


    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def loadDataset(self) -> str:
        pass

    @abstractmethod
    def __call__(self) :
        pass       

    @abstractmethod
    def saveFeatures(self) :
        pass        







