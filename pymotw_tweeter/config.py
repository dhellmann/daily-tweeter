import configparser


def load_config(filename):
    parser = configparser.ConfigParser()
    was_read = parser.read([filename])
    if not was_read:
        raise RuntimeError(
            'Configuration file {} does not exist.'.format(
                filename))
    return parser
