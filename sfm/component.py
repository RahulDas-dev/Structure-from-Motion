"""Abstract Component class."""


import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Optional

from sfm.config.config import Config
from sfm.dataset.dataset import Dataset

logger = logging.getLogger(__name__)


class Component(ABC):
    """Abstract Class for Component Classes."""

    __state: str
    __config: Config
    __chainable: bool

    __next_component: Any

    __slots__ = ("__state", "__height", "__width", "___next_component")

    def __init__(self, state: str, chainable: bool = False):
        super().__init__()
        self.__config = Config.getInstance()
        if state in self.__config.valid_state_names():
            self.__state = state
        else:
            raise Exception(f"State Name {state} is not valid")
        self.__chainable = chainable
        self.__create_output_directory()

    def set_next_component(self, component):
        self.__next_component = component

    @property
    def config(self):
        return self.__config

    def run(self, dataset: Dataset):
        if self.iscompleted(len(dataset)) is False:
            self.move_forward(dataset)
        if self.iscompleted(len(dataset)) is True:
            self.reload(dataset)
        if self.__chainable:
            if isinstance(self.__next_component, Component):
                self.__next_component.run(dataset)
            else:
                logging.error("Next Compent is not Assigned")
                raise Exception("Next Compent is not Assigned")

    @abstractmethod
    def move_forward(self, dataset: Dataset):
        pass

    @abstractmethod
    def reload(self, dataset: Dataset):
        pass

    @property
    def output_directory_path(self) -> str:
        return self.__config.sub_directory_path(self.__state)[0]

    @property
    def output_file(self) -> Optional[str]:
        return self.__config.sub_directory_path(self.__state)[1]

    @property
    def is_output_dir_exists(self):
        return True if os.path.exists(self.output_directory_path) else False

    def __create_output_directory(self):
        if self.is_output_dir_exists is not True:
            os.mkdir(self.output_directory_path, 0o777)

    @abstractmethod
    def iscompleted(self, count: int) -> bool:
        pass
