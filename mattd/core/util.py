import traceback
import logging
log = logging.getLogger("mattd")

def catches_exceptions(f):
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception, e:
            log.error(str(e))
            lines = traceback.format_exc().split('\n')
            map(log.error, lines)

    return wrapper
