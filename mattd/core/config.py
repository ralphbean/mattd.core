import os
import ConfigParser

import logging
log = logging.getLogger("mattd")


def load_config():
    """ Checks ./mattd.d/ and /etc/mattd.d (in that order) and returns a config
    object containing all the configs from those directories.
    """

    dirs = ['./mattd.d', '/etc/mattd.d']
    files = []
    for d in dirs:
        d = os.path.abspath(d)
        try:
            files += [
                d + os.path.sep + fname
                for fname in os.listdir(d)
                if fname.endswith('.ini')
            ]
        except OSError, e:
            pass

    log.info("Loading %i config files: %r" % (len(files), files))
    parser = ConfigParser.SafeConfigParser()
    parser.read(files)
    return parser


def validate_config(config):
    required = {
        'mattd.core': [],
        'logging': ['location', 'level', 'format'],
    }

    for section, items in required.items():
        if not section in config.sections():
            log.error("No [%s] section found in config." % section)
            return False

        for item in items:
            if not item in config.options(section):
                log.error("[%s] has no %r" % (section, item))
                return False

    return True


def extract_logging_config(config):
    """ Returns a dict to configure the logging module.

    See http://bit.ly/U61957 for the schema.
    """
    result = dict(
        version=1,
        handlers={
            'file': {
                'class': "logging.handlers.RotatingFileHandler",
                'formatter': 'awesome_formatter',
                'filename': config.get('logging', 'location') + '/mattd.log',
                'maxBytes': 10485760,
                'backupCount': 2,
            },
        },
        loggers={
            'mattd': {
                'level': config.get('logging', 'level'),
                'handlers': ['file'],
                'propagate': True,
            },
        },
        formatters={
            'awesome_formatter': {
                'format': config.get('logging', 'format'),
            },
        },
    )
    return result
