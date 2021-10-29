""" Helper Functions for Testing Module"""


import json
import os
from shutil import rmtree

_CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_TEST_DIR_PRAENT = os.path.abspath(os.path.join(_CURR_DIR, os.pardir, os.pardir))
TEMP_TEST_DIR = os.path.join(TEMP_TEST_DIR_PRAENT, "temp_test")
CONFIG_JSON_PATH = os.path.join(TEMP_TEST_DIR, "config.json")


def create_temp_test_dir():
    if not os.path.exists(TEMP_TEST_DIR):
        os.mkdir(TEMP_TEST_DIR)


def delete_temp_test_dir():
    if os.path.exists(TEMP_TEST_DIR):
        rmtree(TEMP_TEST_DIR)


def write_config_json(config):
    with open(CONFIG_JSON_PATH, "w") as file:
        json.dump(config, file)


def delete_config_json(config):
    if os.path.exists(CONFIG_JSON_PATH):
        os.remove(CONFIG_JSON_PATH)
