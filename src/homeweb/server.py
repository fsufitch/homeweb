import sys

from pkg_resources import resource_filename
from yaul.daemon import Daemon, run_as_service
from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop

from homeweb.config import get_config
from homeweb.handlers.index import IndexHandler
from homeweb.handlers.about import AboutYouHandler, AboutMeHandler
from homeweb.handlers.contact import ContactInfoHandler
from homeweb.log import setup_logging, ERROR

PATHS = [
         (r'/', IndexHandler),
         (r'/me', AboutMeHandler),
         (r'/you', AboutYouHandler),
         (r'/contact', ContactInfoHandler),
         (r'/s/(.*)', StaticFileHandler, {'path': resource_filename(__name__, 'static')}),
         ]

def runserv(conf):
    setup_logging(conf)
    application = Application(PATHS)
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
