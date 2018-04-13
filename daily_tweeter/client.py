import configparser

import tweepy


def get_client(cfg):
    config_names = [
        'consumer_token',
        'consumer_secret',
        'access_token',
        'access_token_secret',
    ]
    try:
        client_args = {
            name: cfg['user'][name]
            for name in config_names
        }
    except KeyError as e:
        raise RuntimeError(
            'Could not find {!r} in the '
            '[user] section of the config file'.format(
                e.args[0])
        )
    auth = tweepy.OAuthHandler(
        client_args['consumer_token'],
        client_args['consumer_secret'],
    )
    auth.set_access_token(
        client_args['access_token'],
        client_args['access_token_secret'],
    )
    return tweepy.API(auth)
