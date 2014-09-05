import logging

ERROR_LOG_NAME = 'homeweb.log.error'
ACCESS_LOG_NAME = 'homeweb.log.access'
ERROR_LOG = logging.getLogger(ERROR_LOG_NAME)
ACCESS_LOG = logging.getLogger(ACCESS_LOG_NAME)

ERROR = ERROR_LOG
ACCESS = ACCESS_LOG

ERROR_LOG_SETUP = False
ACCESS_LOG_SETUP = False

def make_handler(conf, log_type):
    if conf.get(log_type, 'type')=='file':
        fname = conf.get(log_type, 'destination')
        if not fname:
            raise TypeError('Configuration specifies file logging, but no path given', log_type)
        return logging.FileHandler(fname)
    elif conf.get(log_type, 'type')=='stream':
        return logging.StreamHandler()
    else:
        raise TypeError('Invalid error log type')

def setup_error_logging(conf):
    global ERROR_LOG_SETUP
    LOG = ERROR_LOG
    if ERROR_LOG_SETUP:
        LOG.warn('Attempted to set up error logging twice')
        return

    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,
              }
    chosen_level = levels.get(conf.get('error_log', 'level'), logging.DEBUG)
    LOG.setLevel(chosen_level)

    handler = make_handler(conf, 'error_log')
    handler.setLevel(chosen_level)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    LOG.handlers = []
    LOG.propagate = False
    LOG.addHandler(handler)
    LOG.debug('Error log configured')
    ERROR_LOG_SETUP = True

def setup_access_logging(conf):
    global ACCESS_LOG_SETUP
    LOG = ACCESS_LOG
    if ACCESS_LOG_SETUP:
        ERROR.warn('Attempted to set up access logging twice')
        return
    LOG.setLevel(logging.INFO)
    handler = make_handler(conf, 'access_log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
    LOG.handlers = []
    LOG.propagate = False
    LOG.addHandler(handler)
    ERROR.debug('Access log configured')
    ACCESS_LOG_SETUP = True


def setup_logging(conf):
    setup_error_logging(conf)
    setup_access_logging(conf)