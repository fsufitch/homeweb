from tornado.web import RequestHandler
from homeweb.util import apply_template, write_return

class IndexHandler(RequestHandler):

    @write_return
    @apply_template('index.html')
    def get(self):
        return {}
