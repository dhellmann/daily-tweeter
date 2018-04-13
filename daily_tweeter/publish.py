import datetime
import logging
import os.path

from daily_tweeter import client
from daily_tweeter import config
from daily_tweeter import posts

import appdirs
import tweepy

LOG = logging.getLogger(__name__)


def get_argparse(subparsers):
    default_config_dir = os.path.join(
        appdirs.user_config_dir('daily-tweeter'),
        'config.ini',
    )
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
        func=do_publish,
    )


def safe_tweet(twitter, status, dupe_ok=True):
    LOG.debug('posting %r', status)
    try:
        twitter.update_status(status=status)
    except tweepy.error.TweepError as e:
        LOG.debug('failed: %s', e.reason)
        if dupe_ok and e.api_code == 187:
            return False
        raise RuntimeError('API failure: {}'.format(e.reason))
    return True


def do_publish(args):
    cfg = config.load_config(args.config_file)
    twitter = client.get_client(cfg)
    schedule_data = posts.load_schedule(args.schedule_file)
    today = str(datetime.date.today())
    to_post = schedule_data['by-date'].get(today)
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
