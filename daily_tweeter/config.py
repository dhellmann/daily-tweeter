import configparser
import logging

LOG = logging.getLogger(__name__)


def load_config(filename):
    parser = configparser.ConfigParser()
    logging.debug('reading config from %s', filename)
    was_read = parser.read([filename])
    if not was_read:
        raise RuntimeError(
            'Configuration file {} does not exist.'.format(
                filename))
    return parser
