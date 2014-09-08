from tornado.web import RequestHandler

from homeweb.handlers.demos.diceroll import DicerollHandler
from homeweb.util import apply_template, write_return

class DemoListHandler(RequestHandler):
    demos = [('dice', 'XdY Dice Roller', DicerollHandler),
             ]

    @classmethod
    def get_demo_paths(cls, prefix):
        paths = []
        for demo_id, demo_name, demo_handler in cls.demos:
            path = prefix + demo_id + "/?(.*)"
            entry = (path, demo_handler)
            paths.append(entry)
        return paths

    @write_return
    @apply_template('demolist.html')
    def get(self):
        return {'demos': [(entry[0], entry[1]) for entry in self.__class__.demos]}