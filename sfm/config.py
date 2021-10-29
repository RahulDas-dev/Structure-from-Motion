from typing import List, Union, Dict
import os
import json

from defaultConfig import config as default_config

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
_CONFIG_DIR = os.path.join(_CURRENT_DIR,os.pardir)

_CONFIG_PATH = os.path.join(_CONFIG_DIR,'config.json')

class config(object):

    __config: Dict

    def __init__(self):
        userConfig={}
        with open(_CONFIG_PATH) as file:
            userConfig = json.load(file)
        self.__config = {**default_config, **userConfig}   

    @property
    def feature_extractor(self) -> str:
        return self.__config.get('feature_type')


