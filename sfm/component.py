"""Abstract Component class."""

import os
from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, Type

from sfm.config.config import Config
from sfm.dataset.dataset import Dataset


class Component(ABC):
    """Abstract Class for Component Classes."""

    __state: str
    __config: Type[Config]
    __chainable: bool

    __slots__ = ("__state", "__height", "__width")

    def __init__(self, state: str, chainable=False):
        super().__init__()
        self.__config = Config.getInstance()
        if state in self.__config.valid_state_names():
            self.__state = state
        else:
            raise Exception(f"State Name {state} is not valid")
        self.__chainable = chainable
        self.__create_output_directory()

    @property
    def config(self):
        return self.__config

    def run(self, dataset: Type[Dataset]):
        if self.iscompleted(len(dataset)) is False:
            self.move_forward(dataset)
        if self.__chainable:
            self.next_component().run(dataset)

    @abstractproperty
    def next_component(self):
        pass

    @abstractmethod
    def move_forward(self, dataset: Type[Dataset]):
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

    @abstractproperty
    def iscompleted(self, count: int) -> bool:
        pass
