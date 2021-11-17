"""Main Function to SFM."""

import argparse
import json
import logging
import os
import sys
import traceback
from os import path

import colorlog

from sfm.app import AppEngine
from sfm.config.validator import validate_userdefined_config


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    format = "%(asctime)s:%(name)s - %(message)s"
    date_format = "%H:%M:%S"
    if "colorlog" in sys.modules and os.isatty(2):
        cformat = "%(log_color)s" + format
        formatter = colorlog.ColoredFormatter(
            cformat,
            date_format,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            style="%",
        )
    else:
        formatter = logging.Formatter(format, date_format)
    chenal = logging.StreamHandler()
    chenal.setFormatter(formatter)
    root.addHandler(chenal)


if __name__ == "__main__":
    setup_logging()
    loggger = logging.getLogger(__name__)
    try:
        parser = argparse.ArgumentParser(
            prog="main.py",
            usage="%(prog)s [options]",
            description="""Process SFM on Given Configuration""",
        )
        parser.add_argument(
            "--config",
            default=None,
            dest="config_path",
            action="store",
            help="absolute path of config.json",
        )
        arguments = parser.parse_args()
        config_path = arguments.config_path, arguments.re_start

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

        if validate_userdefined_config(userConfig) is not True:
            raise Exception("User Defind config File is not Valid")

        app_engine = AppEngine(userConfig)
        app_engine.bootstrap()

    except BaseException:
        traceback.print_exc()
        sys.exit(3)
