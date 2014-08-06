from yaul.daemon import Daemon, run_as_service
from tornado.web import Application


class HomeWebDaemon(Daemon):
    def run(self):
        pass

def main_service():
    daemon = HomeWebDaemon('/tmp/homeweb.pid')
    run_as_service(daemon)

def main_cli():
    pass

if __name__ == '__main__':
    main_cli()