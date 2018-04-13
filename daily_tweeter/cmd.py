import argparse
import datetime
import logging
import os.path
import sys

from daily_tweeter import client
from daily_tweeter import config
from daily_tweeter import posts

import appdirs
import tweepy

LOG = logging.getLogger(__name__)


def safe_tweet(twitter, status, dupe_ok=True):
    LOG.debug('posting %r', status)
    try:
        twitter.update_status(status=status)
    except tweepy.error.TweepError as e:
        LOG.debug('failed: %s', e.reason)
        if dupe_ok and e.api_code == 187:
            return False
        raise RuntimeError('API failure: {}'.format(e.reason))


def do_publish(args):
    cfg = config.load_config(args.config_file)
    twitter = client.get_client(cfg)
    post_data = posts.load_posts(args.post_file)
    today = str(datetime.date.today())
    to_post = post_data['by-date'].get(today)
    if not to_post:
        LOG.debug('no post scheduled for %s', today)
        return
    if not safe_tweet(twitter, to_post):
        # Duplicate
        to_post = '{} {}'.format(
            args.repost_prefix,
            to_post,
        )
        safe_tweet(twitter, to_post, dupe_ok=False)


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
        'post_file',
        help='location of YAML file containing posts',
    )
    publish_parser.set_defaults(
        func=do_publish,
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
