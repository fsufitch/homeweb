from yaul.daemon import Daemon, run_as_service
from tornado.web import Application
from tornado.ioloop import IOLoop


class HomeWebDaemon(Daemon):
    def run(self):
        application = Application([(r"/", MainHandler),])
        application.listen(8888)
        IOLoop.instance().start()

def main_service():
    daemon = HomeWebDaemon('/tmp/homeweb.pid')
    run_as_service(daemon)

def main_cli():
    pass

if __name__ == '__main__':
    main_cli()