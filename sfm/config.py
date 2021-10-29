from typing import List, Union, Dict
import os
import json

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
_CONFIG_DIR = os.path.join(_CURRENT_DIR,os.pardir)

_CONFIG_PATH = os.path.join(_CONFIG_DIR,'config.json')

class config(object):

    __config: Dict

    def __init__(self):
        with open(_CONFIG_PATH) as file:
            self.__config = json.load(file)

