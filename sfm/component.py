"""Abstract Component class."""

import os
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Type

from sfm.config.config import Config


class Component(ABC):
    """Abstract Class for Component Classes."""

    __state: str
    __config: Type[Config]

    def __init__(self, config: Type[Config], state: str):
        super().__init__()
        self.__config = config
        if state in config.valid_state_names():
            self.__state = state
        else:
            raise Exception(f"State Name {state} is not valid")
        self.__create_output_directory()

    @abstractmethod
    def run(self):
        pass

    @property
    @lru_cache()
    def output_directory_path(self) -> str:
        return self.__config.sub_directory_path(self.__state)

    @property
    def is_output_dir_exists(self):
        return True if os.path.exists(self.output_directory_path) else False

    def __create_output_directory(self):
        if self.is_output_dir_exists is not True:
            os.mkdir(self.output_directory_path, 0o777)
