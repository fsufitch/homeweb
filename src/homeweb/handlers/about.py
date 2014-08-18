from ipaddress import ip_address
from tornado.web import RequestHandler

from homeweb.util import apply_template, write_return

class AboutYouHandler(RequestHandler):

    @write_return
    @apply_template('about_you.html')
    def get(self):
        ip = ip_address(self.request.remote_ip)
        user_agent = self.request.headers['user-agent']
        return {'ip': ip,
                'user_agent': user_agent,
                }
