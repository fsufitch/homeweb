from yaul.daemon import Daemon, run_as_service
from tornado.web import Application
from tornado.ioloop import IOLoop

from homeweb.handlers.index import IndexHandler

PATHS = [
         (r'/', IndexHandler)
         ]

def runserv():
    application = Application(PATHS)
    application.listen(8888)
    IOLoop.instance().start()

class HomeWebDaemon(Daemon):
    def run(self):
        runserv()

def main_service():
    daemon = HomeWebDaemon('/tmp/homeweb.pid')
    run_as_service(daemon)

def main_cli():
    runserv()

if __name__ == '__main__':
    main_cli()