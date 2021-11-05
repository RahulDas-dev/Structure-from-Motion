""" Helper Functions for Testing Module"""


import json
import os
from shutil import rmtree

import cv2
import numpy as np

_CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_TEST_DIR_PRAENT = os.path.abspath(os.path.join(_CURR_DIR, os.pardir, os.pardir))
TEMP_TEST_DIR = os.path.join(TEMP_TEST_DIR_PRAENT, "temp_test")
CONFIG_JSON_PATH = os.path.join(TEMP_TEST_DIR, "config.json")
DATASET_PATH = os.path.join(TEMP_TEST_DIR, "dataset")
WRONG_DATASET_PATH = os.path.join(TEMP_TEST_DIR, "wrong_dataset")
OUTPUT_PATH = os.path.join(TEMP_TEST_DIR, "output")
WRONG_OUTPUT_PATH = os.path.join(TEMP_TEST_DIR, "wrong_output")


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


def create_temp_dataset_dir():
    if os.path.exists(TEMP_TEST_DIR) is not True:
        os.mkdir(TEMP_TEST_DIR)
    if os.path.exists(DATASET_PATH) is not True:
        os.mkdir(DATASET_PATH)
    else:
        rmtree(DATASET_PATH)
        os.mkdir(DATASET_PATH)


def create_valid_dataset_files():
    if os.path.exists(DATASET_PATH) is not True:
        os.mkdir(DATASET_PATH)
    for i in range(5):
        random_image = np.random.randint(0, 256, size=(300, 300, 3))
        cv2.imwrite(os.path.join(DATASET_PATH, f"image_{i}.jpg"), random_image)
    for i in range(5):
        with open(os.path.join(DATASET_PATH, f"dataset_{i}.text"), "w") as text_file:
            text_file.write("This Is only For Testing")


def create_invalid_dataset_files():
    if os.path.exists(DATASET_PATH) is not True:
        os.mkdir(DATASET_PATH)
    for i in range(5):
        with open(os.path.join(DATASET_PATH, f"dataset_{i}.text"), "w") as text_file:
            text_file.write("This Is only For Testing")


def delete_temp_dataset_dir():
    if os.path.exists(TEMP_TEST_DIR):
        rmtree(TEMP_TEST_DIR)


def create_temp_output_dir(writeble=True):
    if os.path.exists(TEMP_TEST_DIR) is not True:
        os.makedirs(TEMP_TEST_DIR, 0o777 if writeble else 0o400)
    if os.path.exists(OUTPUT_PATH) is not True:
        os.mkdir(OUTPUT_PATH, 0o777 if writeble else 0o400)
    else:
        rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH, 0o777 if writeble else 0o400)


def create_invalid_output_files():
    if os.path.exists(OUTPUT_PATH) is not True:
        os.mkdir(OUTPUT_PATH)
    for i in range(5):
        with open(os.path.join(OUTPUT_PATH, f"output_{i}.text"), "w") as text_file:
            text_file.write("This Is only For Testing")