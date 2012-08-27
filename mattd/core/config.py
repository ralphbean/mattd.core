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
            ]
        except OSError, e:
            pass

    log.info("Loading %i config files: %r" % (len(files), files))
    parser = ConfigParser.SafeConfigParser()
    parser.read(files)
    return parser


def validate_config(config):
    if not 'mattd.core' in config.sections():
        log.error("No [mattd.core] section found in config.")
        return False

    return True
