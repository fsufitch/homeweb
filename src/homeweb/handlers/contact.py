import json
from tornado.web import RequestHandler

from homeweb.config import get_config


class ContactInfoHandler(RequestHandler):
    def error_me_scotty(self):
        self.set_status(404)
        self.set_header('Content-Type', 'text/plain')
        self.write('This is not the contact info you\'re looking for.')

    def get(self):
        self.error_me_scotty()

    def post(self):
        data = self.get_argument('this is a real contact info request')
        print(data)
        if data != 'yup':
            return self.error_me_scotty()

        contact = get_config().get('contact')
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(contact))

