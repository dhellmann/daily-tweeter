import datetime
import logging

from daily_tweeter import client
from daily_tweeter import config
from daily_tweeter import posts

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
