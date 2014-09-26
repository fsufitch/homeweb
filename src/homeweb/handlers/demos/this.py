from tornado.web import RequestHandler

from homeweb.util import apply_template, write_return

class ThisHandler(RequestHandler):
    @write_return
    @apply_template("demos/this.html")
    def get(self, *args):
        return {}
