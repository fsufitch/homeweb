import logging

ERROR_LOG_NAME = 'homeweb.log.error'
ACCESS_LOG_NAME = 'homeweb.log.access'
ERROR_LOG = logging.getLogger(ERROR_LOG_NAME)
ACCESS_LOG = logging.getLogger(ACCESS_LOG_NAME)

ERROR = ERROR_LOG
ACCESS = ACCESS_LOG

ERROR_LOG_SETUP = False
def setup_error_logging(conf):
    global ERROR_LOG_SETUP
    LOG = ERROR_LOG
    if ERROR_LOG_SETUP:
        LOG.warn('Attempted to set up logging twice')
        return
    
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,
              }
    chosen_level = levels.get(conf.get('error_log', 'level'), logging.DEBUG)
    LOG.setLevel(chosen_level)
    
    handler = None
    if conf.get('error_log', 'type')=='file':
        fname = conf.get('error_log', 'destination')
        if not fname:
            raise TypeError('Configuration specifies file error logging, but no path given')
        handler = logging.FileHandler(fname)
    elif conf.get('error_log', 'type')=='stream':
        handler = logging.StreamHandler()
    else:
        raise TypeError('Invalid error log type')
    handler.setLevel(chosen_level)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    LOG.addHandler(handler)
    LOG.debug('Error log configured')
    ERROR_LOG_SETUP = True

def setup_logging(conf):
    setup_error_logging(conf)