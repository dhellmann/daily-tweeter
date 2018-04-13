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
        '--repost-prefix',
        default='Reposting:',
        help='prefix for reposting',
    )
    parser.add_argument(
        '-v',
        action='store_true',
        dest='verbose',
        default=False,
        help='turn on verbose output',
    )
    parser.add_argument(
        'post_file',
        help='location of YAML file containing posts',
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

    post_data = posts.load_posts(args.post_file)
    today = str(datetime.date.today())
    print(post_data, today)
    to_post = post_data['by-date'].get(today)
    if not to_post:
        LOG.debug('no post scheduled for %s', today)
    else:
        LOG.debug('posting %r', to_post)
        try:
            twitter.update_status(status=to_post)
        except tweepy.error.TweepError as e:
            if e.api_code == 187:
                # Duplicate
                to_post = '{} {}'.format(
                    args.repost_prefix,
                    to_post,
                )
                twitter.update_status(status=to_post)
            else:
                raise
