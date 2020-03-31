#!usr/bin/python3

"""
This module functions as entry point for the application
"""

import os

import config
from src import create_app

CONFIG = config.CONFIG_DICT[os.environ["APP_CONFIG"]]

APP = create_app(CONFIG)

if __name__ == "__main__":
    APP.run()
