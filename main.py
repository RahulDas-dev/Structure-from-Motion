"""Main Function to SFM."""

import argparse
import logging
import logging.config
import os

from sfm.app import SFMEnginee

_dir_path = os.path.dirname(os.path.realpath(__file__))
LOGGER_CONFIG_FILE = os.path.join(_dir_path, "logger_config.ini")

parser = argparse.ArgumentParser(
    description="""Runs SFM on given configuration""",
)

parser.add_argument(
    "--config",
    default="config.json",
    dest="config_path",
    help="absolute path of config.json",
)

parser.add_argument(
    "--exp-id",
    type=str,
    default=None,
    dest="exp_id",
    help="experiment_id of old exteriment",
)

parser.add_argument(
    "--log",
    type=str,
    default=None,
    dest="log_dir",
    help="experiment_id of old exteriment",
)

arguments = parser.parse_args()


def main():
    logging.config.fileConfig(LOGGER_CONFIG_FILE, disable_existing_loggers=False)
    # logger = logging.getLogger(__name__)
    # logger.handlers["file_handerler"]["filename"] = "x.log"
    application = SFMEnginee(arguments.config_path, arguments.exp_id)
    application()


if __name__ == "__main__":
    main()
