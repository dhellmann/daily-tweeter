import argparse
import logging
import os.path
import sys

import appdirs

from daily_tweeter import client
from daily_tweeter import config


def main():
    default_config_dir = os.path.join(
        appdirs.user_config_dir('daily-tweeter'),
        'config.ini',
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config-file',
        default=default_config_dir,
        help='location of configuration file',
    )
    parser.add_argument(
        '-v',
        action='store_true',
        dest='verbose',
        default=False,
        help='turn on verbose output',
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s',
        stream=sys.stdout,
    )

    try:
        cfg = config.load_config(args.config_file)
    except Exception as e:
        parser.error(e)

    try:
        twitter = client.get_client(cfg)
    except Exception as e:
        parser.error(e)
