from tornado.web import RequestHandler

from homeweb.util import apply_template, write_return

class ChessBoardHandler(RequestHandler):
    @write_return
    @apply_template("demos/chess.html")
    def get(self):
        return {}
