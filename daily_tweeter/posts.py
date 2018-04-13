import logging

import yaml

LOG = logging.getLogger(__name__)


def load_schedule(filename):
    LOG.debug('reading schedule from %s', filename)
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f.read())
    if data is None:
        data = {}
    posts = data.get('posts', [])
    LOG.debug('found %d entries in post section',
              len(posts))
    # Build the by-date version of the data structure for quick
    # lookup.
    data['by-date'] = {
        p['date']: p['message']
        for p in posts
    }
    return data


def load_posts(filename):
    LOG.debug('reading posts from %s', filename)
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f.read())
    if data is None:
        data = []
    return data
