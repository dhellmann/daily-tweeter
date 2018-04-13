import argparse
import logging
import sys

from daily_tweeter import publish
from daily_tweeter import schedule

LOG = logging.getLogger(__name__)


def main():
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
    publish.get_argparse(subparsers)
    schedule.get_argparse(subparsers)

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
