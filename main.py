"""Main Function to SFM."""


import argparse
import json
import sys
import traceback
from os import path

from sfm.config.validator import validate_userdefined_config

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="main.py", usage="%(prog)s [options]", description="""Process SFM on Given Configuration"""
        )
        parser.add_argument(
            "--config", default=None, dest="config_path", action="store", help="absolute path of config.json"
        )
        parser.add_argument("--re", default=False, dest="re_start", action="store_true", help="Set If want to restart")
        arguments = parser.parse_args()
        config_path, re_start = arguments.config_path, arguments.re_start

        if config_path is None:
            raise ValueError("config_path can not be empty")

        config_path = path.abspath(config_path)

        if path.isfile(config_path) is not True:
            raise FileNotFoundError(f"{config_path} should be valid File")
        if path.basename(config_path).split(".")[-1] != "json":
            raise FileExistsError(f"{config_path} should be json file")

        userConfig = {}
        with open(config_path) as file:
            userConfig = json.load(file)

        if validate_userdefined_config(userConfig, re_start) is not True:
            raise Exception("User Defind config File is not Valid")

    except BaseException:
        traceback.print_exc()
        sys.exit(3)
