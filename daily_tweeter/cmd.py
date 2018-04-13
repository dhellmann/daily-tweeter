import argparse
import os.path

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
    args = parser.parse_args()

    try:
        cfg = config.load_config(args.config_file)
    except Exception as e:
        parser.error(e)

    try:
        twitter = client.get_client(cfg)
    except Exception as e:
        parser.error(e)
