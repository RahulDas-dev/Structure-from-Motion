"""Main Function to SFM."""

import argparse
import os

from sfm.app import SFMEnginee

parser = argparse.ArgumentParser(
    prog="main.py",
    usage="%(prog)s [options]",
    description="""SFM on Given Configuration""",
)

parser.add_argument(
    "--config",
    default=None,
    dest="config_path",
    action="store",
    help="absolute path of config.json",
)

parser.add_argument(
    "--exp-id",
    default=None,
    dest="exp_id",
    action="store",
    help="experiment_id of old exteriment",
)

arguments = parser.parse_args()


def main():
    config_path = os.path.abspath(arguments.config_path)

    application = SFMEnginee(config_path, arguments.exp_id)
    application()
