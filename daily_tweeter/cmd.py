import argparse
import logging
import os.path
import sys

from daily_tweeter import client
from daily_tweeter import config
from daily_tweeter import publish
from daily_tweeter import schedule

import appdirs

LOG = logging.getLogger(__name__)


def main():
    default_config_dir = os.path.join(
        appdirs.user_config_dir('daily-tweeter'),
        'config.ini',
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        action='store_true',
        dest='verbose',
        default=False,
        help='turn on verbose output',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='turn on debug mode',
    )

    subparsers = parser.add_subparsers(help='commands')

    publish_parser = subparsers.add_parser(
        'publish', help='publish a tweet',
    )
    publish_parser.add_argument(
        '-c', '--config-file',
        default=default_config_dir,
        help='location of configuration file',
    )
    publish_parser.add_argument(
        '--repost-prefix',
        default='Reposting:',
        help='prefix for reposting',
    )
    publish_parser.add_argument(
        'schedule_file',
        help='location of schedule file containing posts',
    )
    publish_parser.set_defaults(
        func=publish.do_publish,
    )

    schedule_parser = subparsers.add_parser(
        'schedule', help='build a schedule file',
    )
    schedule_parser.add_argument(
        '-f', '--frequency',
        choices=('daily', 'weekly'),
        default='daily',
        help='how often to schedule posts',
    )
    schedule_parser.add_argument(
        'start_date',
        help='first date to publish, as YYYY-MM-DD',
    )
    schedule_parser.add_argument(
        'post_file',
        help='file containing plain posts',
    )
    schedule_parser.add_argument(
        'schedule_file',
        help='location to write schedule file',
    )
    schedule_parser.set_defaults(
        func=schedule.do_schedule,
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s',
        stream=sys.stdout,
    )

    try:
        args.func(args)
    except Exception as e:
        if args.debug:
            raise
        parser.error(e)
