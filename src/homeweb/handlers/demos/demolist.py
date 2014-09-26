from tornado.web import RequestHandler

from homeweb.handlers.demos.diceroll import DiceRollHandler, OldDiceRollHandler
from homeweb.handlers.demos.chatroom import ChatroomHandler, ChatroomWSHandler
from homeweb.handlers.demos.this import ThisHandler
from homeweb.util import apply_template, write_return

class DemoListHandler(RequestHandler):
    demos = [('dice', 'XdY Dice Roller', DiceRollHandler, True),
             ('olddice', 'Old Dice Roller (offline)', OldDiceRollHandler, True),
             ('chatroom', 'Websocket Chatroom', ChatroomHandler, True),
             ('chatroom_ws', 'Websocket Chatroom (WS)', ChatroomWSHandler, False),
             ('this', 'This Website', ThisHandler, True),
             ]

    @classmethod
    def get_demo_paths(cls, prefix):
        paths = []
        for demo_id, demo_name, demo_handler, demo_show in cls.demos:
            path = prefix + demo_id
            entry = (path, demo_handler)
            paths.append(entry)
        print(paths)
        return paths

    @write_return
    @apply_template('demolist.html')
    def get(self):
        return {'demos': [(entry[0], entry[1]) for entry in self.__class__.demos if entry[3]]}
