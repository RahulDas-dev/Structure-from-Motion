"""Abstract Component class."""


import logging
import os
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, ClassVar, Optional, Type

from sfm.config.config import Config
from sfm.dataset.dataset import Dataset

logger = logging.getLogger(__name__)


class Component(ABC):
    """Abstract Class for Component Classes."""

    __state: ClassVar[str]
    __config: ClassVar[Type[Config]]
    __chainable: ClassVar[bool]

    ___next_component: ClassVar[Any]

    __slots__ = ("__state", "__height", "__width", "___next_component")

    def __init__(self, state: str, chainable=False):
        super().__init__()
        self.__config = Config.getInstance()
        if state in self.__config.valid_state_names():
            self.__state = state
        else:
            raise Exception(f"State Name {state} is not valid")
        self.__chainable = chainable
        self.__create_output_directory()

    def set_next_component(self, component):
        self.___next_component = component

    @property
    def config(self):
        return self.__config

    def run(self, dataset: Type[Dataset]):
        if self.iscompleted(len(dataset)) is False:
            self.move_forward(dataset)
        if self.iscompleted(len(dataset)) is True:
            self.reload(dataset)
        if self.__chainable:
            if isinstance(self.___next_component, Component):
                self.___next_component.run(dataset)
            else:
                logging.error("Next Compent is not Assigned")
                raise Exception("Next Compent is not Assigned")

    @abstractmethod
    def move_forward(self, dataset: Type[Dataset]):
        pass

    @abstractmethod
    def reload(self, dataset: Type[Dataset]):
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
