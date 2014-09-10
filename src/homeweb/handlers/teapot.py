from pkg_resources import resource_filename
from tornado.web import RequestHandler
from homeweb.util import apply_template, write_return

class TeapotHandler(RequestHandler):
    def get(self):
        with open(resource_filename("homeweb", "resources/teapot.txt")) as f:
            tea = f.read()
        self.set_status(418, "I'm a teapot")
        self.set_header("Content-Type", "text/plain")
        self.write(tea)
