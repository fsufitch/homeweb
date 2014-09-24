import json
from datetime import datetime

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from homeweb.util import apply_template, write_return

##### Data model stuff

MAX_MESSAGE_BACKLOG = 1000

class Chatroom(object):
    _SINGLETON = None
    @classmethod
    def get(cls):
        if not cls._SINGLETON:
            cls._SINGLETON = Chatroom()
        return cls._SINGLETON

    def __init__(self):
        self.messages = []
        self.users = {}

    def add_message(self, date, user, message):
        self.messages.append( (date, user, message) )
        if len(self.messages) > MAX_MESSAGE_BACKLOG:
            num_to_delete = len(self.messages) - MAX_MESSAGE_BACKLOG
            self.messages = self.messages[num_to_delete:]

    def send_message(self, from_user, message):
        date = datetime.utcnow()
        for to_user in self.users.values():
            to_user.send_message(date, from_user, message)
        self.add_message(date, from_user, message)

class User(object):
    def __init__(self, username, ws_handler):
        self.username = username
        self.ws_handler = ws_handler

    def send_message(self, date, from_user, message):
        self.ws_handler.outgoing_message(date, from_user, message)

##### Web stuff

class ChatroomHandler(RequestHandler):
    @write_return
    @apply_template("demos/chatroom.html")
    def get(self, *args):
        path = self.request.full_url().replace('http://', 'ws://')
        path = '/'.join(path.split('/')[:-1]) # Strip off the last bit
        path += '/chatroom_ws'
        return {'ws_path': path}


class ChatroomWSHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.user = None
        self.chatroom = Chatroom.get()
        super(ChatroomWSHandler, self).__init__(*args, **kwargs)

    def open(self):
        print("ws opened!")

    def on_message(self, msg):
        decoded = json.loads(msg)
        ACTIONS = {'init_chat': self.init_chat,
                   'message': self.process_message,
                   }
        if decoded.get('action') not in ACTIONS:
            raise ValueError('Unknown action:', decoded.get('action'))
        ACTIONS[decoded.get('action')](decoded)

    def init_chat(self, data):
        username = data.get('username', '')
        if not username or username in self.chatroom.users:
            msg = json.dumps({'action': 'error', 'data': 'Name invalid, try again'})
            self.write_message(msg)
            return
        self.user = User(username, self)
        self.chatroom.users[username] = self.user
        self.write_message(json.dumps({'action': 'init_success'}))

    def process_message(self, data):
        message = data.get('message', '')
        if not message:
            return
        if len(message)>300:
            msg = json.dumps({'action': 'error', 'data': 'Message too long (%d > 300)' % len(message)})
            self.write_message(msg)
            return
        self.chatroom.send_message(self.user, message)

    def outgoing_message(self, date, from_user, message):
        data = { 'action': 'send_message',
                 'data': {'date': date.strftime("%Y-%m-%d %H:%M:%S"),
                          'username': from_user.username,
                          'message': message
                          }
                }
        self.write_message(json.dumps(data))
