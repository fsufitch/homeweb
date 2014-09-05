import json, time, sys

from pkg_resources import resource_filename
from yaul.daemon import Daemon, run_as_service
from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop

from homeweb.config import get_config
from homeweb.handlers.index import IndexHandler
from homeweb.handlers.about import AboutYouHandler, AboutMeHandler
from homeweb.handlers.contact import ContactInfoHandler
from homeweb.log import setup_logging, ERROR, ACCESS

PATHS = [
         (r'/', IndexHandler),
         (r'/me', AboutMeHandler),
         (r'/you', AboutYouHandler),
         (r'/contact', ContactInfoHandler),
         (r'/s/(.*)', StaticFileHandler, {'path': resource_filename(__name__, 'static')}),
         ]

FORBID_HEADERS = ['Cookie', 'If-None-Match']

def log_request(request_handler):
    print("hello! "+str(request_handler))
    request = request_handler.request
    headers = dict(request.headers)

    for header_name in FORBID_HEADERS:
        if header_name in headers:
            del headers[header_name]

    output = {
              'time': time.time(),
              'method': request.method,
              'uri': request.uri,
              'remote_ip': request.remote_ip,
              'protocol': request.protocol,
              'host': request.host,
              'request_time': request.request_time(),
              'headers': dict(request.headers),
              }
    ACCESS.info(json.dumps(output))

def runserv(conf):
    setup_logging(conf)
    application = Application(PATHS, log_function=log_request)
    port = conf.get('listen', 'port')
    host = conf.get('listen', 'host') or ''
    ERROR.info('Listening on \'%s\', port %s' % (host, port))
    application.listen(port, address=host)
    ERROR.info('Starting IO loop...')
    IOLoop.instance().start()

class HomeWebDaemon(Daemon):
    def __init__(self, conf):
        super(HomeWebDaemon, self).__init__(conf.get('pidpath'))
        self.conf = conf

    def run(self):
        runserv(self.conf)

def main_service():
    conf = get_config(generate=True)
    daemon = HomeWebDaemon(conf)
    run_as_service(daemon)

def main_cli():
    confpath = None
    if len(sys.argv)>1:
        confpath = sys.argv[1]
    conf = get_config(generate=True, confpath=confpath)
    runserv(conf)
